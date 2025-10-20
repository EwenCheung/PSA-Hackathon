"""Seed test data for mentoring system development."""
import json
from datetime import datetime, timedelta
from app.core.db import get_connection


def seed_test_data():
    """Add comprehensive test data for mentors, mentees, and mentorship relationships."""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("🌱 Seeding test data...")
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"⚠️  Database already has {count} employees. Skipping seed.")
        return
    
    # ============================================================================
    # DEPARTMENTS
    # ============================================================================
    departments = [
        ('DEPT001', 'Engineering', 'Software Development'),
        ('DEPT002', 'Data Science', 'ML and Analytics'),
        ('DEPT003', 'Product', 'Product Management'),
        ('DEPT004', 'Design', 'UX/UI Design'),
        ('DEPT005', 'Operations', 'IT Operations'),
    ]
    
    for dept_id, name, description in departments:
        cursor.execute("""
            INSERT OR IGNORE INTO departments (id, name, description)
            VALUES (?, ?, ?)
        """, (dept_id, name, description))
    
    print(f"✅ Added {len(departments)} departments")
    
    # ============================================================================
    # SKILLS
    # ============================================================================
    skills = [
        ('SKILL001', 'Python', 'Programming', 'Python programming language'),
        ('SKILL002', 'JavaScript', 'Programming', 'JavaScript programming language'),
        ('SKILL003', 'React', 'Frontend', 'React.js framework'),
        ('SKILL004', 'Node.js', 'Backend', 'Node.js runtime'),
        ('SKILL005', 'AWS', 'Cloud', 'Amazon Web Services'),
        ('SKILL006', 'Azure', 'Cloud', 'Microsoft Azure'),
        ('SKILL007', 'Machine Learning', 'Data Science', 'ML algorithms and models'),
        ('SKILL008', 'Data Analysis', 'Data Science', 'Data analysis and visualization'),
        ('SKILL009', 'Leadership', 'Soft Skills', 'Team leadership'),
        ('SKILL010', 'System Design', 'Architecture', 'System architecture design'),
        ('SKILL011', 'Docker', 'DevOps', 'Container technology'),
        ('SKILL012', 'Kubernetes', 'DevOps', 'Container orchestration'),
        ('SKILL013', 'SQL', 'Database', 'SQL databases'),
        ('SKILL014', 'Product Strategy', 'Product', 'Product strategy and planning'),
        ('SKILL015', 'UI/UX Design', 'Design', 'User interface and experience'),
    ]
    
    for skill_id, name, category, description in skills:
        cursor.execute("""
            INSERT OR IGNORE INTO skills (id, name, category, description)
            VALUES (?, ?, ?, ?)
        """, (skill_id, name, category, description))
    
    print(f"✅ Added {len(skills)} skills")
    
    # ============================================================================
    # SENIOR MENTORS (High expertise)
    # ============================================================================
    mentors = [
        {
            'id': 'EMP001',
            'name': 'Dr. Sarah Chen',
            'email': 'sarah.chen@psa.com',
            'role': 'Principal Engineer',
            'department_id': 'DEPT001',
            'level': 'Principal',
            'hire_date': '2015-03-15',
            'skills_map': json.dumps({
                'Python': 5, 'System Design': 5, 'AWS': 4, 'Leadership': 5,
                'Machine Learning': 4, 'Docker': 4
            }),
            'goals_set': json.dumps(['Mentor junior engineers', 'Scale ML platform']),
            # Mentor profile
            'is_mentor': 1,
            'capacity': 4,
            'mentees_count': 2,
            'rating': 4.9,
            'personality': 'Patient, technical depth, great at explaining complex concepts'
        },
        {
            'id': 'EMP002',
            'name': 'Marcus Rodriguez',
            'email': 'marcus.r@psa.com',
            'role': 'Senior Software Architect',
            'department_id': 'DEPT001',
            'level': 'Senior',
            'hire_date': '2016-07-20',
            'skills_map': json.dumps({
                'System Design': 5, 'AWS': 5, 'Python': 4, 'Node.js': 4,
                'Kubernetes': 5, 'Leadership': 4
            }),
            'goals_set': json.dumps(['Transition to VP Engineering']),
            'is_mentor': 1,
            'capacity': 3,
            'mentees_count': 1,
            'rating': 4.8,
            'personality': 'Strategic thinker, excellent at architecture patterns'
        },
        {
            'id': 'EMP003',
            'name': 'Jennifer Wu',
            'email': 'jennifer.wu@psa.com',
            'role': 'Lead Data Scientist',
            'department_id': 'DEPT002',
            'level': 'Senior',
            'hire_date': '2017-01-10',
            'skills_map': json.dumps({
                'Machine Learning': 5, 'Python': 5, 'Data Analysis': 5,
                'SQL': 4, 'AWS': 3
            }),
            'goals_set': json.dumps(['Build AI Center of Excellence']),
            'is_mentor': 1,
            'capacity': 3,
            'mentees_count': 2,
            'rating': 4.7,
            'personality': 'Research-oriented, loves teaching ML concepts'
        },
        {
            'id': 'EMP004',
            'name': 'David Kim',
            'email': 'david.kim@psa.com',
            'role': 'Senior Frontend Engineer',
            'department_id': 'DEPT001',
            'level': 'Senior',
            'hire_date': '2018-05-12',
            'skills_map': json.dumps({
                'React': 5, 'JavaScript': 5, 'UI/UX Design': 4,
                'System Design': 3, 'Node.js': 3
            }),
            'goals_set': json.dumps(['Lead frontend architecture']),
            'is_mentor': 1,
            'capacity': 4,
            'mentees_count': 1,
            'rating': 4.6,
            'personality': 'Creative, great at UI/UX mentoring'
        },
        {
            'id': 'EMP005',
            'name': 'Aisha Patel',
            'email': 'aisha.patel@psa.com',
            'role': 'Senior Product Manager',
            'department_id': 'DEPT003',
            'level': 'Senior',
            'hire_date': '2017-09-01',
            'skills_map': json.dumps({
                'Product Strategy': 5, 'Leadership': 5, 'Data Analysis': 4,
                'UI/UX Design': 3
            }),
            'goals_set': json.dumps(['Grow product team', 'Launch new product line']),
            'is_mentor': 1,
            'capacity': 3,
            'mentees_count': 2,
            'rating': 4.8,
            'personality': 'User-focused, strategic, excellent communicator'
        },
    ]
    
    # ============================================================================
    # MID-LEVEL EMPLOYEES (Potential mentees)
    # ============================================================================
    mid_level = [
        {
            'id': 'EMP010',
            'name': 'Alex Thompson',
            'email': 'alex.t@psa.com',
            'role': 'Software Engineer',
            'department_id': 'DEPT001',
            'level': 'Mid',
            'hire_date': '2021-03-15',
            'skills_map': json.dumps({
                'Python': 3, 'React': 3, 'SQL': 3, 'AWS': 2
            }),
            'goals_set': json.dumps([
                'Become Senior Engineer',
                'Learn system design',
                'Lead a project team'
            ]),
            'is_mentor': 0,
            'capacity': 0,
            'mentees_count': 0,
            'rating': 0.0,
            'personality': ''
        },
        {
            'id': 'EMP011',
            'name': 'Priya Sharma',
            'email': 'priya.s@psa.com',
            'role': 'Data Analyst',
            'department_id': 'DEPT002',
            'level': 'Mid',
            'hire_date': '2021-06-20',
            'skills_map': json.dumps({
                'Python': 3, 'Data Analysis': 4, 'SQL': 4, 'Machine Learning': 2
            }),
            'goals_set': json.dumps([
                'Transition to Data Scientist role',
                'Master ML algorithms',
                'Deploy production ML model'
            ]),
            'is_mentor': 0,
            'capacity': 0,
            'mentees_count': 0,
            'rating': 0.0,
            'personality': ''
        },
        {
            'id': 'EMP012',
            'name': 'James Wilson',
            'email': 'james.w@psa.com',
            'role': 'Frontend Developer',
            'department_id': 'DEPT001',
            'level': 'Mid',
            'hire_date': '2022-01-10',
            'skills_map': json.dumps({
                'JavaScript': 4, 'React': 3, 'UI/UX Design': 2
            }),
            'goals_set': json.dumps([
                'Learn advanced React patterns',
                'Improve system design skills',
                'Mentor junior developers'
            ]),
            'is_mentor': 0,
            'capacity': 0,
            'mentees_count': 0,
            'rating': 0.0,
            'personality': ''
        },
    ]
    
    # ============================================================================
    # JUNIOR EMPLOYEES (Actively seeking mentorship)
    # ============================================================================
    juniors = [
        {
            'id': 'EMP020',
            'name': 'Emma Garcia',
            'email': 'emma.g@psa.com',
            'role': 'Junior Software Engineer',
            'department_id': 'DEPT001',
            'level': 'Junior',
            'hire_date': '2024-01-15',
            'skills_map': json.dumps({
                'Python': 2, 'JavaScript': 2, 'SQL': 2
            }),
            'goals_set': json.dumps([
                'Build full-stack applications',
                'Learn cloud deployment',
                'Contribute to open source'
            ]),
            'is_mentor': 0,
            'capacity': 0,
            'mentees_count': 0,
            'rating': 0.0,
            'personality': ''
        },
        {
            'id': 'EMP021',
            'name': 'Michael Chang',
            'email': 'michael.c@psa.com',
            'role': 'Junior Data Analyst',
            'department_id': 'DEPT002',
            'level': 'Junior',
            'hire_date': '2024-03-01',
            'skills_map': json.dumps({
                'Python': 2, 'SQL': 3, 'Data Analysis': 2
            }),
            'goals_set': json.dumps([
                'Learn machine learning',
                'Master data visualization',
                'Present insights to stakeholders'
            ]),
            'is_mentor': 0,
            'capacity': 0,
            'mentees_count': 0,
            'rating': 0.0,
            'personality': ''
        },
    ]
    
    # Insert all employees and their mentorship profiles
    all_employees = mentors + mid_level + juniors
    
    for emp in all_employees:
        # Insert employee
        cursor.execute("""
            INSERT INTO employees (
                id, name, email, role, department_id, level, hire_date,
                skills_map, goals_set
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            emp['id'], emp['name'], emp['email'], emp['role'],
            emp['department_id'], emp['level'], emp['hire_date'],
            emp['skills_map'], emp['goals_set']
        ))
        
        # Insert mentorship profile
        cursor.execute("""
            INSERT INTO mentorship_profiles (
                employee_id, is_mentor, capacity, mentees_count, rating, personality
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            emp['id'], emp['is_mentor'], emp['capacity'],
            emp['mentees_count'], emp['rating'], emp['personality']
        ))
    
    print(f"✅ Added {len(all_employees)} employees ({len(mentors)} mentors)")
    
    # ============================================================================
    # ACTIVE MENTORSHIP PAIRS
    # ============================================================================
    start_date = datetime.now() - timedelta(days=90)
    
    mentorship_pairs = [
        {
            'id': 'PAIR001',
            'mentor_id': 'EMP001',  # Dr. Sarah Chen
            'mentee_id': 'EMP020',  # Emma Garcia
            'start_date': start_date.strftime('%Y-%m-%d'),
            'status': 'active',
            'focus_areas': json.dumps(['Python', 'System Design', 'Career Growth']),
            'goals': json.dumps([
                'Build scalable REST API',
                'Learn design patterns',
                'Prepare for mid-level promotion'
            ]),
            'progress': 65,
            'sessions_completed': 8
        },
        {
            'id': 'PAIR002',
            'mentor_id': 'EMP003',  # Jennifer Wu
            'mentee_id': 'EMP011',  # Priya Sharma
            'start_date': (start_date + timedelta(days=15)).strftime('%Y-%m-%d'),
            'status': 'active',
            'focus_areas': json.dumps(['Machine Learning', 'Python', 'Data Science']),
            'goals': json.dumps([
                'Complete ML certification',
                'Deploy first ML model',
                'Present at data science meetup'
            ]),
            'progress': 45,
            'sessions_completed': 5
        },
        {
            'id': 'PAIR003',
            'mentor_id': 'EMP004',  # David Kim
            'mentee_id': 'EMP012',  # James Wilson
            'start_date': (start_date + timedelta(days=30)).strftime('%Y-%m-%d'),
            'status': 'active',
            'focus_areas': json.dumps(['React', 'Frontend Architecture', 'UI/UX']),
            'goals': json.dumps([
                'Master React hooks and context',
                'Lead frontend feature',
                'Improve design skills'
            ]),
            'progress': 30,
            'sessions_completed': 3
        },
    ]
    
    for pair in mentorship_pairs:
        cursor.execute("""
            INSERT INTO mentorship_matches (
                id, mentor_id, mentee_id, start_date, status,
                focus_areas, goals, progress
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pair['id'], pair['mentor_id'], pair['mentee_id'],
            pair['start_date'], pair['status'], pair['focus_areas'],
            pair['goals'], pair['progress']
        ))
    
    print(f"✅ Added {len(mentorship_pairs)} active mentorship pairs")
    
    # ============================================================================
    # MENTOR SESSIONS
    # ============================================================================
    sessions = [
        # Sarah Chen + Emma Garcia sessions
        {
            'mentor_id': 'EMP001',
            'mentee_id': 'EMP020',
            'date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'duration': 60,
            'topics': json.dumps(['REST API design', 'Database optimization']),
            'notes': 'Discussed API best practices and database indexing',
            'rating': 5
        },
        {
            'mentor_id': 'EMP001',
            'mentee_id': 'EMP020',
            'date': (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d'),
            'duration': 45,
            'topics': json.dumps(['Design patterns', 'Code review']),
            'notes': 'Reviewed singleton and factory patterns',
            'rating': 5
        },
        # Jennifer Wu + Priya Sharma sessions
        {
            'mentor_id': 'EMP003',
            'mentee_id': 'EMP011',
            'date': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
            'duration': 60,
            'topics': json.dumps(['ML algorithms', 'Feature engineering']),
            'notes': 'Covered decision trees and feature selection techniques',
            'rating': 5
        },
    ]
    
    for session in sessions:
        cursor.execute("""
            INSERT INTO mentor_sessions (
                mentor_id, mentee_id, session_date, duration_minutes,
                topics_covered, notes, mentee_rating
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session['mentor_id'], session['mentee_id'], session['date'],
            session['duration'], session['topics'], session['notes'],
            session['rating']
        ))
    
    print(f"✅ Added {len(sessions)} mentor sessions")
    
    conn.commit()
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "="*60)
    print("🎉 DATABASE SEEDED SUCCESSFULLY!")
    print("="*60)
    
    cursor.execute("SELECT COUNT(*) FROM departments")
    print(f"📁 Departments: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM skills")
    print(f"🔧 Skills: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM employees")
    print(f"👥 Employees: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM mentorship_profiles WHERE is_mentor = 1")
    print(f"🎓 Mentors: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM mentorship_matches WHERE status = 'active'")
    print(f"🤝 Active Pairs: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM mentor_sessions")
    print(f"📅 Sessions: {cursor.fetchone()[0]}")
    
    print("\n✨ You can now test:")
    print("   - Find mentors: skill_area='Python', min_rating=4.5")
    print("   - Get recommendations for: employee_id='EMP020'")
    print("   - Check progress for: pair_id='PAIR001'")
    print("="*60 + "\n")


if __name__ == "__main__":
    seed_test_data()
