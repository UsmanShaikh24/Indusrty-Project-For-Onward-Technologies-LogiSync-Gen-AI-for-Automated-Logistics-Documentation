from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String, unique=True, index=True)
    start_location = Column(String)
    end_location = Column(String)
    waypoints = Column(JSON)  # Store multiple stops
    cargo_details = Column(JSON)  # Store cargo information
    time_constraints = Column(JSON)  # Store pickup/delivery windows
    fuel_stops = Column(JSON)  # Recommended fuel stops
    compliance_checkpoints = Column(JSON)  # Required inspection/rest points
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deliveries = relationship("Delivery", back_populates="route")

class Delivery(Base):
    __tablename__ = "deliveries"
    
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(String)  # pending, in_progress, completed, delayed
    estimated_delivery_time = Column(DateTime)
    actual_delivery_time = Column(DateTime)
    delay_reason = Column(String, nullable=True)
    proof_of_delivery = Column(String, nullable=True)  # File path or URL
    route = relationship("Route", back_populates="deliveries")
    customer = relationship("Customer", back_populates="deliveries")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(String)
    communication_preferences = Column(JSON)  # Store preferred notification methods
    deliveries = relationship("Delivery", back_populates="customer")

class ComplianceDocument(Base):
    __tablename__ = "compliance_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    document_type = Column(String)  # FMCSA, safety_inspection, environmental, driver_qualification
    related_route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)
    content = Column(JSON)  # Store document content
    file_path = Column(String)  # Path to generated document
    created_at = Column(DateTime)
    expiry_date = Column(DateTime, nullable=True)
    status = Column(String)  # draft, submitted, approved, expired