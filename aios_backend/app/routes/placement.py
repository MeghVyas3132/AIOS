from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from app.core.database import get_db
from app.core.deps import get_current_user, require_student
from app.models.user import User
from app.models.placement import PlacementProfile
from app.schemas import PlacementProfileCreate, PlacementProfileUpdate, PlacementProfileResponse
from app.services.placement_service import (
    create_or_update_placement_profile, get_placement_profile,
    get_students_by_domain, get_top_students_by_domain,
    analyze_placement_profile
)

router = APIRouter(prefix="/api/placement", tags=["Placement"])


@router.post("/profile", response_model=PlacementProfileResponse)
async def create_placement_profile(
    profile_data: PlacementProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    """
    Create or update student placement profile
    Uses rule-based logic to determine best-fit domain
    """
    try:
        profile = create_or_update_placement_profile(
            db,
            student_id=current_user.id,
            skills=profile_data.skills,
            projects=profile_data.projects,
            cgpa=profile_data.cgpa,
            experience=profile_data.experience,
        )
        
        # Parse JSON fields for response
        profile.skills = json.loads(profile.skills) if isinstance(profile.skills, str) else profile.skills
        profile.projects = json.loads(profile.projects) if profile.projects and isinstance(profile.projects, str) else profile.projects
        profile.domain_scores = json.loads(profile.domain_scores) if isinstance(profile.domain_scores, str) else profile.domain_scores
        
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/profile", response_model=PlacementProfileResponse)
async def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    """Get current student's placement profile"""
    profile = get_placement_profile(db, current_user.id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Placement profile not found. Please create one first.",
        )
    
    # Parse JSON fields for response
    profile.skills = json.loads(profile.skills) if isinstance(profile.skills, str) else profile.skills
    profile.projects = json.loads(profile.projects) if profile.projects and isinstance(profile.projects, str) else profile.projects
    profile.domain_scores = json.loads(profile.domain_scores) if isinstance(profile.domain_scores, str) else profile.domain_scores
    
    return profile


@router.post("/analyze")
async def analyze_skills(
    profile_data: PlacementProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    """
    Analyze skills and get best-fit domain recommendation
    Does not save the profile
    """
    try:
        analysis = analyze_placement_profile(
            db,
            current_user.id,
            profile_data.skills,
            profile_data.projects,
            profile_data.cgpa,
            profile_data.experience,
        )
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/domain/{domain}", response_model=List[PlacementProfileResponse])
async def get_students_by_best_fit_domain(
    domain: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all students for a specific domain"""
    profiles = get_students_by_domain(db, domain)
    
    # Parse JSON fields for response
    for profile in profiles:
        profile.skills = json.loads(profile.skills) if isinstance(profile.skills, str) else profile.skills
        profile.projects = json.loads(profile.projects) if profile.projects and isinstance(profile.projects, str) else profile.projects
        profile.domain_scores = json.loads(profile.domain_scores) if isinstance(profile.domain_scores, str) else profile.domain_scores
    
    return profiles


@router.get("/domain/{domain}/top", response_model=List[PlacementProfileResponse])
async def get_top_students_in_domain(
    domain: str,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get top students by CGPA in a specific domain"""
    profiles = get_top_students_by_domain(db, domain, limit)
    
    # Parse JSON fields for response
    for profile in profiles:
        profile.skills = json.loads(profile.skills) if isinstance(profile.skills, str) else profile.skills
        profile.projects = json.loads(profile.projects) if profile.projects and isinstance(profile.projects, str) else profile.projects
        profile.domain_scores = json.loads(profile.domain_scores) if isinstance(profile.domain_scores, str) else profile.domain_scores
    
    return profiles
