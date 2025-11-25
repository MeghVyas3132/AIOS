from sqlalchemy.orm import Session
from typing import Dict, List
import json
from app.models.placement import PlacementProfile
from app.core.config import DOMAIN_KEYWORDS


def analyze_placement_profile(
    db: Session,
    student_id: int,
    skills: List[str],
    projects: List[str] = None,
    cgpa: float = None,
    experience: str = None,
) -> Dict:
    """
    Analyze student placement profile and determine best-fit domain
    Rule-based logic: Skill matching with domain categories
    """
    # Parse skills (handle case-insensitivity and partial matches)
    skills_lower = [skill.lower() for skill in skills]
    
    # Calculate domain scores
    domain_scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        domain_keywords_lower = [kw.lower() for kw in keywords]
        
        # Count matches
        matches = 0
        for skill in skills_lower:
            for keyword in domain_keywords_lower:
                if keyword in skill or skill in keyword:
                    matches += 1
        
        # Calculate score (0-100)
        if len(skills) > 0:
            score = (matches / len(domain_keywords_lower)) * 100
            # Normalize: if more than 100, cap it
            score = min(score, 100)
        else:
            score = 0
        
        domain_scores[domain] = round(score, 2)
    
    # Determine best-fit domain
    best_fit_domain = max(domain_scores, key=domain_scores.get) if domain_scores else None
    best_fit_score = max(domain_scores.values()) if domain_scores else 0
    
    # If best fit score is too low, consider it as "Generalist"
    if best_fit_score < 20:
        best_fit_domain = "Generalist"
    
    return {
        "best_fit_domain": best_fit_domain,
        "domain_scores": domain_scores,
        "analysis": f"Based on your skills, {best_fit_domain} is the best fit domain for you.",
    }


def create_or_update_placement_profile(
    db: Session,
    student_id: int,
    skills: List[str],
    projects: List[str] = None,
    cgpa: float = None,
    experience: str = None,
) -> PlacementProfile:
    """Create or update placement profile for a student"""
    
    # Check if profile exists
    profile = db.query(PlacementProfile).filter(
        PlacementProfile.student_id == student_id
    ).first()
    
    # Analyze profile
    analysis = analyze_placement_profile(db, student_id, skills, projects, cgpa, experience)
    
    if profile:
        # Update existing profile
        profile.skills = json.dumps(skills)
        profile.projects = json.dumps(projects) if projects else None
        profile.cgpa = cgpa if cgpa else profile.cgpa
        profile.experience = experience if experience else profile.experience
        profile.best_fit_domain = analysis["best_fit_domain"]
        profile.domain_scores = json.dumps(analysis["domain_scores"])
    else:
        # Create new profile
        profile = PlacementProfile(
            student_id=student_id,
            skills=json.dumps(skills),
            projects=json.dumps(projects) if projects else None,
            cgpa=cgpa or 0.0,
            experience=experience,
            best_fit_domain=analysis["best_fit_domain"],
            domain_scores=json.dumps(analysis["domain_scores"]),
        )
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    
    return profile


def get_placement_profile(db: Session, student_id: int) -> PlacementProfile:
    """Get placement profile for a student"""
    return db.query(PlacementProfile).filter(
        PlacementProfile.student_id == student_id
    ).first()


def get_students_by_domain(db: Session, domain: str) -> List[PlacementProfile]:
    """Get all students for a specific domain"""
    profiles = db.query(PlacementProfile).filter(
        PlacementProfile.best_fit_domain == domain
    ).all()
    return profiles


def get_top_students_by_domain(db: Session, domain: str, limit: int = 10) -> List[PlacementProfile]:
    """Get top students by CGPA for a specific domain"""
    profiles = db.query(PlacementProfile).filter(
        PlacementProfile.best_fit_domain == domain
    ).order_by(PlacementProfile.cgpa.desc()).limit(limit).all()
    return profiles
