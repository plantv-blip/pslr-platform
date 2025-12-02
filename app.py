#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PSLR Platform v3.0 - Production Version
Physical-Spiritual-Logical-Relational Framework for LLM Cognitive Analysis

Features:
- PostgreSQL database integration
- RESTful API
- 3D visualization
- Batch data collection
- Production-ready deployment

Author: PSLR Research Team
License: MIT
"""

from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import re

# Import our modules
from config import get_config
from models import db, PSLRAnalysis, BatchExperiment
from llm_clients import PSLRAnalyzer

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(get_config())

# Initialize extensions
CORS(app, origins=app.config['CORS_ORIGINS'])
db.init_app(app)
migrate = Migrate(app, db)

# Create tables on startup
with app.app_context():
    db.create_all()

# Initialize PSLR Analyzer
analyzer = PSLRAnalyzer()

# HTML Template (same as before, with DB integration)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PSLR Live Platform - LLM 인지 편향 실시간 측정</title>
    <script src="https://cdn.jsdelivr.net/npm/vue@3.3.4/dist/vue.global.prod.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            min-height: 100vh;
        }
        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            color: #333;
        }
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        #canvas-3d {
            width: 100%;
            height: 500px;
            border-radius: 8px;
            background: #000;
        }
        .btn-primary {
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
        }
        .btn-primary:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .input-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .input-group input, .input-group select {
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 1em;
        }
        .results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .result-card {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
        }
        .pslr-values {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 15px;
        }
        .pslr-item {
            background: white;
            padding: 10px;
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
        }
        .pslr-label {
            font-weight: 600;
            color: #555;
        }
        .pslr-value {
            font-size: 1.2em;
            font-weight: 700;
            color: #667eea;
        }
        .loading {
            text-align: center;
            padding: 40px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .stats-bar {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }
        .stat-item {
            text-align: center;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            flex: 1;
            margin: 0 10px;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div id="app" class="container">
        <header>
            <h1>🔮 PSLR Live Platform</h1>
            <p>Physical-Spiritual-Logical-Relational Framework for LLM Cognitive Bias Analysis</p>
            <p style="font-size:0.9em; margin-top:10px;">
                논문: <a href="/paper" style="color:#ffd700;">Cognitive Spectrum Analysis of LLMs Using PSLR Methodology</a>
            </p>
            <div class="stats-bar" style="margin-top:20px;">
                <div class="stat-item">
                    <div class="stat-number">{{ stats.total_analyses }}</div>
                    <div class="stat-label">Total Analyses</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{{ stats.total_concepts }}</div>
                    <div class="stat-label">Unique Concepts</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{{ stats.total_models }}</div>
                    <div class="stat-label">Models Tested</div>
                </div>
            </div>
        </header>

        <!-- 3D Visualization -->
        <div class="card">
            <h2>🌐 3D PSLR 시각화</h2>
            <div id="canvas-3d"></div>
        </div>

        <!-- Analysis Controls -->
        <div class="card">
            <h2>⚙️ 실시간 분석</h2>
            <div class="input-group">
                <input v-model="concept" placeholder="분석할 개념 입력 (예: Love, AI, Freedom)">
                <select v-model="selectedModel">
                    <option value="">모델 선택</option>
                    <option value="gpt-4o">GPT-4o</option>
                    <option value="claude">Claude-3.5-Sonnet</option>
                    <option value="gemini">Gemini-2.0-Flash</option>
                    <option value="deepseek">DeepSeek-V3</option>
                    <option value="grok">Grok-2</option>
                </select>
                <input v-model="apiKey" type="password" placeholder="API Key">
                <button class="btn-primary" @click="analyze" :disabled="loading">
                    {{ loading ? '분석 중...' : '분석 시작' }}
                </button>
            </div>
        </div>

        <!-- History -->
        <div class="card">
            <h2>📜 분석 히스토리</h2>
            <div class="input-group">
                <select v-model="historyFilter">
                    <option value="">모든 모델</option>
                    <option value="gpt-4o">GPT-4o</option>
                    <option value="claude">Claude</option>
                    <option value="gemini">Gemini</option>
                    <option value="deepseek">DeepSeek</option>
                    <option value="grok">Grok</option>
                </select>
                <input v-model="conceptFilter" placeholder="개념 검색">
                <button class="btn-primary" @click="loadHistory">검색</button>
            </div>
        </div>

        <!-- Results -->
        <div class="card" v-if="results.length > 0">
            <h2>📊 분석 결과</h2>
            <div class="results-grid">
                <div class="result-card" v-for="result in results" :key="result.id">
                    <h3>{{ result.model_name }}</h3>
                    <p style="color:#888; font-size:0.9em;">{{ result.concept }} ({{ result.language }})</p>
                    <div class="pslr-values">
                        <div class="pslr-item">
                            <span class="pslr-label">P (Physical)</span>
                            <span class="pslr-value">{{ result.result.P.toFixed(2) }}</span>
                        </div>
                        <div class="pslr-item">
                            <span class="pslr-label">S (Spiritual)</span>
                            <span class="pslr-value">{{ result.result.S.toFixed(2) }}</span>
                        </div>
                        <div class="pslr-item">
                            <span class="pslr-label">L (Logical)</span>
                            <span class="pslr-value">{{ result.result.L.toFixed(2) }}</span>
                        </div>
                        <div class="pslr-item">
                            <span class="pslr-label">R (Relational)</span>
                            <span class="pslr-value">{{ result.result.R.toFixed(2) }}</span>
                        </div>
                    </div>
                    <p style="margin-top:15px; font-size:0.9em; color:#666;">
                        {{ result.result.reasoning }}
                    </p>
                    <p style="margin-top:10px; font-size:0.8em; color:#999;">
                        {{ new Date(result.timestamp).toLocaleString() }}
                    </p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const { createApp } = Vue;

        // Three.js objects outside Vue reactivity
        let threeScene, threeCamera, threeRenderer, threeSphere;

        function init3D() {
            const container = document.getElementById('canvas-3d');
            if (!container) return;

            threeScene = new THREE.Scene();
            threeCamera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
            threeCamera.position.z = 5;

            threeRenderer = new THREE.WebGLRenderer({ antialias: true });
            threeRenderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(threeRenderer.domElement);

            const geometry = new THREE.SphereGeometry(2, 32, 32);
            const material = new THREE.MeshNormalMaterial({ wireframe: false });
            threeSphere = new THREE.Mesh(geometry, material);
            threeScene.add(threeSphere);

            const light = new THREE.PointLight(0xffffff, 1, 100);
            light.position.set(10, 10, 10);
            threeScene.add(light);

            const controls = new THREE.OrbitControls(threeCamera, threeRenderer.domElement);
            controls.enableDamping = true;

            animate3D();
        }

        function animate3D() {
            requestAnimationFrame(animate3D);
            if (threeSphere) {
                threeSphere.rotation.x += 0.005;
                threeSphere.rotation.y += 0.005;
            }
            if (threeRenderer && threeScene && threeCamera) {
                threeRenderer.render(threeScene, threeCamera);
            }
        }

        function updateSphere(pslr) {
            if (threeSphere) {
                const scale = (pslr.P + pslr.S + pslr.L + pslr.R) / 2;
                threeSphere.scale.set(scale, scale, scale);
            }
        }

        createApp({
            data() {
                return {
                    concept: '',
                    selectedModel: 'gpt-4o',
                    apiKey: '',
                    loading: false,
                    results: [],
                    stats: {
                        total_analyses: 0,
                        total_concepts: 0,
                        total_models: 0
                    },
                    historyFilter: '',
                    conceptFilter: ''
                };
            },

            mounted() {
                init3D();
                this.loadStats();
                this.loadHistory();
            },

            methods: {
                
                async loadStats() {
                    try {
                        const response = await fetch('/api/stats');
                        this.stats = await response.json();
                    } catch (error) {
                        console.error('Failed to load stats:', error);
                    }
                },
                
                async analyze() {
                    if (!this.concept || !this.apiKey) {
                        alert('개념과 API 키를 입력해주세요.');
                        return;
                    }
                    
                    this.loading = true;
                    
                    try {
                        const response = await fetch('/api/analyze', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                concept: this.concept,
                                model: this.selectedModel,
                                language: 'en',
                                api_key: this.apiKey
                            })
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            this.results.unshift(result);
                            updateSphere(result.result);
                            this.loadStats();
                        } else {
                            alert('분석 실패: ' + result.error);
                        }
                    } catch (error) {
                        alert('오류: ' + error.message);
                    } finally {
                        this.loading = false;
                    }
                },
                
                async loadHistory() {
                    try {
                        let url = '/api/history?limit=20';
                        if (this.historyFilter) url += `&model=${this.historyFilter}`;
                        if (this.conceptFilter) url += `&concept=${this.conceptFilter}`;

                        const response = await fetch(url);
                        this.results = await response.json();
                    } catch (error) {
                        console.error('Failed to load history:', error);
                    }
                }
            }
        }).mount('#app');
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page"""
    return HTML_TEMPLATE


@app.route('/api/analyze', methods=['POST'])
def analyze_concept():
    """Analyze a concept and save to database"""
    data = request.json
    concept = data.get('concept', '').strip()
    model = data.get('model', 'gpt-4o')
    language = data.get('language', 'en')
    api_key = data.get('api_key', '')
    
    if not concept or not api_key:
        return jsonify({"success": False, "error": "Missing required fields"}), 400
    
    # Perform analysis
    result = analyzer.analyze(concept, language, model, api_key)
    
    if result['success']:
        # Save to database
        analysis = PSLRAnalysis(
            concept=concept,
            language=language,
            model=model,
            model_name=result['model_name'],
            p_value=result['result']['P'],
            s_value=result['result']['S'],
            l_value=result['result']['L'],
            r_value=result['result']['R'],
            reasoning=result['result']['reasoning'],
            raw_response=result.get('raw_response', ''),
            response_time=result.get('response_time', 0)
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        # Return with database ID
        result['id'] = analysis.id
    
    return jsonify(result)


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get analysis history from database"""
    limit = request.args.get('limit', 20, type=int)
    model = request.args.get('model', None)
    concept = request.args.get('concept', None)
    
    query = PSLRAnalysis.query
    
    if model:
        query = query.filter_by(model=model)
    
    if concept:
        query = query.filter(PSLRAnalysis.concept.ilike(f'%{concept}%'))
    
    analyses = query.order_by(PSLRAnalysis.created_at.desc()).limit(limit).all()
    
    return jsonify([a.to_dict() for a in analyses])


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get platform statistics"""
    total_analyses = PSLRAnalysis.query.count()
    total_concepts = db.session.query(PSLRAnalysis.concept).distinct().count()
    total_models = db.session.query(PSLRAnalysis.model).distinct().count()
    
    return jsonify({
        'total_analyses': total_analyses,
        'total_concepts': total_concepts,
        'total_models': total_models
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500


@app.route('/paper')
def paper():
    """Link to paper"""
    return """
    <html>
    <head><title>PSLR Paper</title></head>
    <body style="font-family: sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;">
        <h1>📄 Cognitive Spectrum Analysis of Large Language Models Using PSLR Scan Methodology</h1>
        <p><strong>Author:</strong> Young (Independent AI Research)</p>
        <p><strong>Date:</strong> November 2025</p>
        <p><strong>Version:</strong> 1.0 - Final Integration</p>
        <hr>
        <p>This paper introduces the PSLR (Physical-Spiritual-Logical-Relational) framework for analyzing 
        cognitive patterns in large language models.</p>
        <p><a href="/">← Back to Platform</a></p>
    </body>
    </html>
    """


# Database initialization
@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("✅ Database initialized successfully!")


if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║           PSLR Platform v3.0 - Production                    ║
║                                                               ║
║  🌐 Server starting on:                                      ║
║      http://0.0.0.0:5000                                     ║
║                                                               ║
║  📊 Database: PostgreSQL (Production) / SQLite (Dev)         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(app.config['FLASK_ENV'] == 'development'))
