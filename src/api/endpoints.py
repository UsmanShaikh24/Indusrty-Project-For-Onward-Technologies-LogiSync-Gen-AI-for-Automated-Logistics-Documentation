from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

from ..services.route_optimizer import RouteOptimizer
from ..services.document_generator import DocumentGenerator
from ..models.database import Route, Delivery, Customer, ComplianceDocument
from ..database import get_db

router = APIRouter()
route_optimizer = RouteOptimizer()
document_generator = DocumentGenerator()

@router.post("/routes/optimize")
async def optimize_route(
    locations: List[str],
    cargo_details: Dict[str, Any],
    time_constraints: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Optimize route and generate route documentation"""
    try:
        # Optimize route
        route_plan = route_optimizer.optimize_route(locations, cargo_details, time_constraints)
        
        if not route_plan:
            raise HTTPException(status_code=400, detail="Could not optimize route with given constraints")
        
        # Generate route documentation
        route_doc = await document_generator.generate_route_document(route_plan)
        
        # Save route to database
        new_route = Route(
            route_name=f"Route_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            start_location=locations[0],
            end_location=locations[-1],
            waypoints=locations[1:-1],
            cargo_details=cargo_details,
            time_constraints=time_constraints,
            fuel_stops=route_plan["fuel_stops"],
            compliance_checkpoints=route_plan["compliance_checkpoints"],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.add(new_route)
        db.commit()
        db.refresh(new_route)
        
        return {
            "route_id": new_route.id,
            "route_plan": route_plan,
            "documentation_path": route_doc
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/customer-communications/{notification_type}")
async def generate_customer_communication(
    notification_type: str,
    delivery_id: int,
    db: Session = Depends(get_db)
):
    """Generate personalized customer communications"""
    try:
        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
        if not delivery:
            raise HTTPException(status_code=404, detail="Delivery not found")
        
        customer = db.query(Customer).filter(Customer.id == delivery.customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        delivery_data = {
            "delivery_date": delivery.estimated_delivery_time.date(),
            "time_window": f"{delivery.estimated_delivery_time.strftime('%H:%M')} - {delivery.estimated_delivery_time.strftime('%H:%M')}",
            "tracking_number": f"TRK{delivery.id:06d}",
            "tracking_url": f"https://logisync.com/track/{delivery.id}",
            "delay_reason": delivery.delay_reason,
            "new_delivery_time": delivery.estimated_delivery_time,
            "delivery_time": delivery.actual_delivery_time,
            "pod_reference": delivery.proof_of_delivery
        }
        
        customer_data = {
            "customer_name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "communication_preferences": customer.communication_preferences
        }
        
        message = await document_generator.generate_customer_notification(
            notification_type,
            delivery_data,
            customer_data
        )
        
        return {"message": message}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compliance-documents/{document_type}")
async def generate_compliance_document(
    document_type: str,
    data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Generate regulatory compliance documents"""
    try:
        # Generate document
        doc_path = await document_generator.generate_compliance_report(document_type, data)
        
        # Save document record to database
        new_doc = ComplianceDocument(
            document_type=document_type,
            related_route_id=data.get("route_id"),
            content=data,
            file_path=doc_path,
            created_at=datetime.now(),
            expiry_date=data.get("expiry_date"),
            status="draft"
        )
        
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
        
        return {
            "document_id": new_doc.id,
            "file_path": doc_path,
            "status": "generated"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))