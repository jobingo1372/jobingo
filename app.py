from flask import Flask, render_template, request, redirect, url_for
import os, csv

app = Flask(__name__)

# ---------------- Resume Upload ----------------
# Uploads folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ========================
# POST RESUME
# ========================
@app.route('/post-resume', methods=['GET', 'POST'])
def post_resume():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        job_title = request.form.get('job_title', '')  # hidden field

        file = request.files.get('resume')

        if file and file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            file_exists = os.path.isfile('resumes.csv')
            with open('resumes.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['Name', 'Email', 'Job Title', 'Resume File'])
                writer.writerow([name, email, job_title, file.filename])

            return "✅ Resume uploaded successfully!"

        return "❌ Please select a file!"
    
    # agar GET request hai to form show karega
    job_title = request.args.get("job_title", "")
    return render_template('post_resume.html', job_title=job_title)


if __name__ == "__main__":
    app.run(debug=True)



# ---------------- Job Posting ----------------
@app.route("/post-job", methods=["GET", "POST"])
def post_job():
    if request.method == "POST":
        title = request.form.get("title")
        role = request.form.get("role")
        industry = request.form.get("industry")
        company = request.form.get("company")
        location = request.form.get("location")
        experience = request.form.get("experience")
        salary = request.form.get("salary")
        education = request.form.get("education")
        description = request.form.get("description")

        # Create CSV if not exists
        if not os.path.exists("jobs.csv"):
            with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Title","Role","Industry","Company","Location","Experience","Salary","Education","Description"])

        # Append job
        with open("jobs.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([title, role, industry, company, location, experience, salary, education, description])

        return redirect(url_for("view_jobs"))

    return render_template("post_job.html")


# ---------------- View Jobs ----------------
@app.route("/jobs")
def view_jobs():
    jobs = []
    if os.path.exists("jobs.csv"):
        with open("jobs.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) != 9:
                    continue  # Skip incomplete rows
                jobs.append({
                    "Title": row[0],
                    "Role": row[1],
                    "Industry": row[2],
                    "Company": row[3],
                    "Location": row[4],
                    "Experience": row[5],
                    "Salary": row[6],
                    "Education": row[7],
                    "Description": row[8]
                })
    return render_template("view_jobs.html", jobs=jobs)


# ---------------- Apply Job ----------------
@app.route("/apply/<title>", methods=["GET", "POST"])
def apply_job(title):
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        resume = request.form.get("resume")

        # Create CSV if not exists
        if not os.path.exists("applications.csv"):
            with open("applications.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["JobTitle","CandidateName","Email","Resume"])

        # Append application
        with open("applications.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([title, name, email, resume])

        return f"Thank you {name}, your application for {title} has been submitted!"

    return render_template("apply_job.html", title=title)


# ---------------- Home ----------------
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
