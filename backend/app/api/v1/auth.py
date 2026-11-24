from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.db.session import get_db
from backend.app.models.entities import User, Role
from backend.app.core.security import verify_password, create_access_token, get_password_hash
from backend.app.schemas.common import (
    LoginRequest, RegisterRequest, TokenResponse, UserResponse, StudentProfileUpdateRequest
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        (User.username == payload.username) | (User.email == payload.username)
    ).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    role_name = user.role.name if user.role else "student"
    token = create_access_token({"sub": user.id, "username": user.username, "role": role_name})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        email=user.email,
        role=role_name,
        full_name=user.full_name or user.username,
        roll_number=getattr(user, "roll_number", "") or "",
        department=getattr(user, "department", "CSE (AI)") or "CSE (AI)",
        semester=getattr(user, "semester", "Sem 5 (CSE - AI)") or "Sem 5 (CSE - AI)",
        cgpa=getattr(user, "cgpa", "8.0") or "8.0",
        resume_url=getattr(user, "resume_url", "") or "",
        skills=getattr(user, "skills", "") or "",
        phone=getattr(user, "phone", "") or ""
    )

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    target_role = "admin" if (payload.role or "").lower() == "admin" else "student"

    # Derive username if omitted
    username = payload.username
    if not username or not username.strip():
        if target_role == "admin":
            username = payload.email.split("@")[0]
        else:
            username = payload.roll_number.strip() if payload.roll_number and payload.roll_number.strip() else payload.email.split("@")[0]

    existing = db.query(User).filter(
        (User.username == username) | (User.email == payload.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is already registered."
        )

    # Resolve or create role
    role_obj = db.query(Role).filter(Role.name == target_role).first()
    if not role_obj:
        role_obj = Role(name=target_role, description=f"{target_role.capitalize()} Role")
        db.add(role_obj)
        db.flush()

    if target_role == "admin":
        full_name = payload.full_name or "System Administrator"
        dept = "Academic Administration"
        sem = "Faculty / Admin"
        cgpa_val = "N/A"
        roll_val = ""
        resume_val = ""
        skills_val = ""
    else:
        full_name = payload.full_name or username
        dept = payload.department or "CSE (AI)"
        sem = payload.semester or "Sem 5 (CSE - AI)"
        cgpa_val = payload.cgpa or "8.0"
        roll_val = payload.roll_number or ""
        resume_val = payload.resume_url or ""
        skills_val = payload.skills or ""

    new_user = User(
        username=username,
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        full_name=full_name,
        role_id=role_obj.id,
        roll_number=roll_val,
        department=dept,
        semester=sem,
        cgpa=cgpa_val,
        resume_url=resume_val,
        skills=skills_val,
        phone=payload.phone or ""
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.id, "username": new_user.username, "role": target_role})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        role=target_role,
        full_name=new_user.full_name,
        roll_number=new_user.roll_number,
        department=new_user.department,
        semester=new_user.semester,
        cgpa=new_user.cgpa,
        resume_url=new_user.resume_url,
        skills=new_user.skills,
        phone=new_user.phone
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(user_id: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(User)
    if user_id:
        user = query.filter(User.id == user_id).first()
    else:
        user = query.filter(User.username == "surya").first() or query.first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role.name if user.role else "student",
        roll_number=user.roll_number or "",
        department=user.department or "CSE (AI)",
        semester=user.semester or "Sem 5",
        cgpa=user.cgpa or "8.0",
        resume_url=user.resume_url or "",
        skills=user.skills or "",
        phone=user.phone or ""
    )

@router.put("/profile", response_model=UserResponse)
def update_student_profile(
    payload: StudentProfileUpdateRequest,
    user_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(User)
    if user_id:
        user = query.filter(User.id == user_id).first()
    else:
        user = query.filter(User.username == "surya").first()

    if not user:
        raise HTTPException(status_code=404, detail="Student profile not found")

    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.roll_number is not None:
        user.roll_number = payload.roll_number
    if payload.department is not None:
        user.department = payload.department
    if payload.semester is not None:
        user.semester = payload.semester
    if payload.cgpa is not None:
        user.cgpa = payload.cgpa
    if payload.resume_url is not None:
        user.resume_url = payload.resume_url
    if payload.skills is not None:
        user.skills = payload.skills
    if payload.phone is not None:
        user.phone = payload.phone

    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role.name if user.role else "student",
        roll_number=user.roll_number or "",
        department=user.department or "CSE (AI)",
        semester=user.semester or "Sem 5",
        cgpa=user.cgpa or "8.0",
        resume_url=user.resume_url or "",
        skills=user.skills or "",
        phone=user.phone or ""
    )
