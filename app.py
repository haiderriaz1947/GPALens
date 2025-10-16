import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="GPA & CGPA Calculator ",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .gpa-display {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
    }
    .grade-table {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def calculate_gpa(marks, credit_hours, grading_scale):
    """Calculate GPA based on marks and credit hours"""
    total_credits = 0
    total_grade_points = 0
    
    for mark, credit in zip(marks, credit_hours):
        grade_point, grade = convert_to_grade_point(mark, grading_scale)
        total_grade_points += grade_point * credit
        total_credits += credit
    
    if total_credits == 0:
        return 0, 0
    gpa = total_grade_points / total_credits
    return gpa, total_credits

def convert_to_grade_point(mark, scale):
 
    if scale == "4.0 Scale (Pakistan)":
        if mark >= 85:
            return 4.0, "A"
        elif mark >= 80:
            return 3.7, "A-"
        elif mark >= 75:
            return 3.3, "B+"
        elif mark >= 70:
            return 3.0, "B"
        elif mark >= 65:
            return 2.7, "B-"
        elif mark >= 61:
            return 2.3, "C+"
        elif mark >= 58:
            return 2.0, "C"
        elif mark >= 55:
            return 1.7, "C-"
        elif mark >= 50:
            return 1.0, "D"
        else:
            return 0.0, "F"
    else:  # Percentage Scale
        # For percentage scale, we'll use direct percentage as base
        if mark >= 85:
            return 4.0, "A"
        elif mark >= 80:
            return 3.7, "A-"
        elif mark >= 75:
            return 3.3, "B+"
        elif mark >= 70:
            return 3.0, "B"
        elif mark >= 65:
            return 2.7, "B-"
        elif mark >= 61:
            return 2.3, "C+"
        elif mark >= 58:
            return 2.0, "C"
        elif mark >= 55:
            return 1.7, "C-"
        elif mark >= 50:
            return 1.0, "D"
        else:
            return 0.0, "F"

def get_grade_description(grade):
    """Get description for each grade"""
    grade_descriptions = {
        "A": "Excellent",
        "A-": "Very Good",
        "B+": "Good Plus",
        "B": "Good",
        "B-": "Satisfactory Plus",
        "C+": "Satisfactory",
        "C": "Acceptable",
        "C-": "Acceptable Minus",
        "D": "Pass",
        "F": "Fail"
    }
    return grade_descriptions.get(grade, "")

def main():
    # Main header
    st.markdown('<div class="main-header">🎓 GPA & CGPA Calculator </div>', unsafe_allow_html=True)
    
    # Display Pakistani Grading System
    st.markdown("---")
    st.markdown("### 📋  Grading System")
    
    grading_data = {
        "Marks (%)": ["85-100", "80-84", "75-79", "70-74", "65-69", "61-64", "58-60", "55-57", "50-54", "Below 50"],
        "Grade": ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"],
        "Grade Points": ["4.0", "3.7", "3.3", "3.0", "2.7", "2.3", "2.0", "1.7", "1.0", "0.0"],
        "Description": ["Excellent", "Very Good", "Good Plus", "Good", "Satisfactory Plus", 
                       "Satisfactory", "Acceptable", "Acceptable Minus", "Pass", "Fail"]
    }
    
    grading_df = pd.DataFrame(grading_data)
    st.dataframe(grading_df, use_container_width=True, hide_index=True)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose Calculator", 
                                   ["Single Semester GPA", "Multiple Semesters CGPA"])
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Pakistani Grading Scale:**
    - A: 85-100% (4.0)
    - A-: 80-84% (3.7)
    - B+: 75-79% (3.3)
    - B: 70-74% (3.0)
    - B-: 65-69% (2.7)
    - C+: 61-64% (2.3)
    - C: 58-60% (2.0)
    - C-: 55-57% (1.7)
    - D: 50-54% (1.0)
    - F: Below 50% (0.0)
    """)
    
    if app_mode == "Single Semester GPA":
        single_semester_gpa()
    else:
        multiple_semesters_cgpa()

def single_semester_gpa():
    st.markdown('<div class="sub-header">📚 Single Semester GPA Calculator</div>', unsafe_allow_html=True)
    
    # Grading scale selection
    col1, col2 = st.columns(2)
    with col1:
        grading_scale = st.selectbox(
            "Select Grading Scale",
            ["4.0 Scale (Pakistan)", "Percentage Scale"],
            help="4.0 Scale: Standard Pakistani University System"
        )
    
    with col2:
        num_subjects = st.number_input(
            "Number of Subjects",
            min_value=1,
            max_value=20,
            value=5,
            step=1
        )
    
    st.markdown("### Enter Subject Details")
    
    # Create input fields for subjects
    subjects_data = []
    marks_list = []
    credits_list = []
    
    for i in range(num_subjects):
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            subject_name = st.text_input(f"Subject {i+1} Name", value=f"Subject {i+1}", key=f"name_{i}")
        with col2:
            marks = st.number_input(
                f"Marks (%)", 
                min_value=0.0, 
                max_value=100.0, 
                value=75.0, 
                step=0.5,
                key=f"marks_{i}"
            )
        with col3:
            credit_hours = st.number_input(
                f"Credit Hours", 
                min_value=1.0, 
                max_value=5.0, 
                value=3.0, 
                step=0.5,
                key=f"credit_{i}"
            )
        
        grade_point, grade = convert_to_grade_point(marks, grading_scale)
        
        subjects_data.append({
            'Subject': subject_name,
            'Marks': marks,
            'Credit Hours': credit_hours,
            'Grade': grade,
            'Grade Points': grade_point,
            'Description': get_grade_description(grade)
        })
        marks_list.append(marks)
        credits_list.append(credit_hours)
    
    # Calculate GPA
    if st.button("Calculate GPA", type="primary"):
        gpa, total_credits = calculate_gpa(marks_list, credits_list, grading_scale)
        
        # Display results
        st.markdown("---")
        st.markdown('<div class="sub-header">📊 Results</div>', unsafe_allow_html=True)
        
        # Display subjects table
        df = pd.DataFrame(subjects_data)
        st.dataframe(df, use_container_width=True)
        
        # Display GPA
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.metric("Total Credit Hours", f"{total_credits}")
            st.metric("Total Subjects", f"{num_subjects}")
            st.metric("Grading Scale", "Pakistani 4.0 Scale")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(f'<div class="gpa-display">GPA: {gpa:.2f}/4.0</div>', unsafe_allow_html=True)
            
            # Grade interpretation for Pakistani system
            if gpa >= 3.7:
                st.success("🏆 Excellent! First Class with Distinction")
            elif gpa >= 3.3:
                st.success("🎉 Very Good! First Class")
            elif gpa >= 3.0:
                st.info("👍 Good! Second Class Upper")
            elif gpa >= 2.5:
                st.info("📚 Satisfactory! Second Class Lower")
            elif gpa >= 2.0:
                st.warning("✅ Acceptable! Third Class")
            elif gpa >= 1.0:
                st.warning("⚠️ Pass")
            else:
                st.error("❌ Fail - Needs Improvement")
            
            st.markdown('</div>', unsafe_allow_html=True)

def multiple_semesters_cgpa():
    st.markdown('<div class="sub-header">🎓 Multiple Semesters CGPA Calculator</div>', unsafe_allow_html=True)
    
    # Grading scale selection
    grading_scale = st.selectbox(
        "Select Grading Scale",
        ["4.0 Scale (Pakistan)", "Percentage Scale"],
        help="4.0 Scale: Standard Pakistani University System",
        key="cgpa_scale"
    )
    
    num_semesters = st.number_input(
        "Number of Semesters",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )
    
    semesters_data = []
    semester_gpas = []
    semester_credits_list = []
    
    for sem in range(num_semesters):
        st.markdown(f"### Semester {sem + 1} Details")
        
        col1, col2 = st.columns(2)
        with col1:
            num_subjects = st.number_input(
                f"Number of Subjects in Semester {sem + 1}",
                min_value=1,
                max_value=15,
                value=5,
                step=1,
                key=f"sem_{sem}_subjects"
            )
        
        semester_marks = []
        semester_credits = []
        
        for i in range(num_subjects):
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                subject_name = st.text_input(
                    f"Sem {sem+1} - Subject {i+1}", 
                    value=f"Sem {sem+1} Subject {i+1}",
                    key=f"sem{sem}_name_{i}"
                )
            with col2:
                marks = st.number_input(
                    f"Marks (%)", 
                    min_value=0.0, 
                    max_value=100.0, 
                    value=75.0, 
                    step=0.5,
                    key=f"sem{sem}_marks_{i}"
                )
            with col3:
                credit_hours = st.number_input(
                    f"Credit Hours", 
                    min_value=1.0, 
                    max_value=5.0, 
                    value=3.0, 
                    step=0.5,
                    key=f"sem{sem}_credit_{i}"
                )
            
            semester_marks.append(marks)
            semester_credits.append(credit_hours)
        
        # Calculate semester GPA
        sem_gpa, total_credits = calculate_gpa(semester_marks, semester_credits, grading_scale)
        
        semesters_data.append({
            'Semester': sem + 1,
            'GPA': sem_gpa,
            'Total Credits': total_credits,
            'Subjects': num_subjects
        })
        
        semester_gpas.append(sem_gpa)
        semester_credits_list.append(total_credits)
        
        st.info(f"Semester {sem + 1} GPA: {sem_gpa:.2f}/4.0 | Total Credits: {total_credits} | Subjects: {num_subjects}")
        st.markdown("---")
    
    # Calculate CGPA
    if st.button("Calculate CGPA", type="primary"):
        total_credits_all = sum(semester_credits_list)
        weighted_gpa_sum = sum(gpa * credits for gpa, credits in zip(semester_gpas, semester_credits_list))
        
        if total_credits_all > 0:
            cgpa = weighted_gpa_sum / total_credits_all
        else:
            cgpa = 0
        
        # Display results
        st.markdown("---")
        st.markdown('<div class="sub-header">📈 CGPA Results</div>', unsafe_allow_html=True)
        
        # Display semesters summary
        df = pd.DataFrame(semesters_data)
        st.dataframe(df, use_container_width=True)
        
        # Display CGPA
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.metric("Total Semesters", num_semesters)
            st.metric("Total Credits", f"{total_credits_all}")
            st.metric("Average GPA", f"{np.mean(semester_gpas):.2f}/4.0")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(f'<div class="gpa-display">CGPA: {cgpa:.2f}/4.0</div>', unsafe_allow_html=True)
            
            # CGPA interpretation for Pakistani system
            if cgpa >= 3.7:
                st.success("🏆 Outstanding! First Class with Distinction")
            elif cgpa >= 3.3:
                st.success("🎉 Excellent! First Class")
            elif cgpa >= 3.0:
                st.info("👍 Very Good! Second Class Upper")
            elif cgpa >= 2.5:
                st.info("📚 Good! Second Class Lower")
            elif cgpa >= 2.0:
                st.warning("✅ Satisfactory! Third Class")
            elif cgpa >= 1.0:
                st.warning("⚠️ Pass")
            else:
                st.error("❌ Overall Fail - Serious Improvement Needed")
            
            # Calculate percentage equivalent (approximate)
            percentage_approx = (cgpa / 4.0) * 100
            st.metric("Approximate Percentage", f"{percentage_approx:.1f}%")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
