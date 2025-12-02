#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Models for PSLR Platform
SQLAlchemy ORM models for storing analysis results
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON

db = SQLAlchemy()


class PSLRAnalysis(db.Model):
    """PSLR 분석 결과 저장"""
    __tablename__ = 'pslr_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Analysis metadata
    concept = db.Column(db.String(200), nullable=False, index=True)
    language = db.Column(db.String(10), nullable=False, default='en')
    model = db.Column(db.String(50), nullable=False, index=True)
    model_name = db.Column(db.String(100), nullable=False)
    
    # PSLR values
    p_value = db.Column(db.Float, nullable=False)  # Physical
    s_value = db.Column(db.Float, nullable=False)  # Spiritual
    l_value = db.Column(db.Float, nullable=False)  # Logical
    r_value = db.Column(db.Float, nullable=False)  # Relational
    
    # Additional data
    reasoning = db.Column(db.Text)
    raw_response = db.Column(db.Text)
    response_time = db.Column(db.Integer)  # milliseconds
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Metadata (JSON for flexibility)
    metadata = db.Column(JSON)
    
    def to_dict(self):
        """Convert to dictionary for API response"""
        return {
            'id': self.id,
            'concept': self.concept,
            'language': self.language,
            'model': self.model,
            'model_name': self.model_name,
            'timestamp': self.created_at.isoformat(),
            'result': {
                'P': self.p_value,
                'S': self.s_value,
                'L': self.l_value,
                'R': self.r_value,
                'reasoning': self.reasoning
            },
            'response_time': self.response_time,
            'raw_response': self.raw_response
        }
    
    def __repr__(self):
        return f'<PSLRAnalysis {self.concept} by {self.model_name}>'


class BatchExperiment(db.Model):
    """배치 실험 추적"""
    __tablename__ = 'batch_experiments'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Experiment metadata
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    total_concepts = db.Column(db.Integer)
    total_models = db.Column(db.Integer)
    total_analyses = db.Column(db.Integer)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    progress = db.Column(db.Integer, default=0)
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Results summary (JSON)
    summary = db.Column(JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'total_concepts': self.total_concepts,
            'total_models': self.total_models,
            'total_analyses': self.total_analyses,
            'status': self.status,
            'progress': self.progress,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'summary': self.summary
        }
    
    def __repr__(self):
        return f'<BatchExperiment {self.name} - {self.status}>'
