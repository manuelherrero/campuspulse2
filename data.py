import pandas as pd
import random
from datetime import datetime, timedelta

# ─── UNIVERSITIES ─────────────────────────────────────────────────────────────
UNIVERSITIES = {
    "Universidad Complutense de Madrid": {
        "acronym": "UCM", "district": "Moncloa", "campus": "Ciudad Universitaria"
    },
    "Universidad Autónoma de Madrid": {
        "acronym": "UAM", "district": "Cantoblanco", "campus": "Cantoblanco Campus"
    },
    "Universidad Carlos III de Madrid": {
        "acronym": "UC3M", "district": "Leganés / Getafe", "campus": "Leganés Campus"
    },
    "Universidad Politécnica de Madrid": {
        "acronym": "UPM", "district": "Moncloa", "campus": "Montegancedo Campus"
    },
    "Universidad Rey Juan Carlos": {
        "acronym": "URJC", "district": "Móstoles / Alcorcón", "campus": "Móstoles Campus"
    },
    "Universidad de Alcalá": {
        "acronym": "UAH", "district": "Alcalá de Henares", "campus": "Historic Campus"
    },
    "Universidad Nebrija": {
        "acronym": "UNEB", "district": "La Dehesa", "campus": "La Dehesa Campus"
    },
    "Universidad Pontificia Comillas": {
        "acronym": "COMILLAS", "district": "Alberto Aguilera", "campus": "Alberto Aguilera Campus"
    },
    "IE University Madrid": {
        "acronym": "IE", "district": "Salamanca", "campus": "Madrid Campus"
    },
    "Universidad Francisco de Vitoria": {
        "acronym": "UFV", "district": "Pozuelo de Alarcón", "campus": "Pozuelo Campus"
    },
}

# ─── TOPICS ───────────────────────────────────────────────────────────────────
TOPICS = {
    "Technology & AI": {
        "emoji": "🤖",
        "color": "#47c8ff",
        "events": [
            {
                "title": "Artificial Intelligence Hackathon 2025",
                "description": "48 hours of intensive coding to solve real-world challenges with AI. Teams of 2 to 4 people. Mentors from Google, Amazon and local startups will be available. Cash prizes and job interviews for winners.",
                "duration": "48h",
                "price": 0,
                "format": "In-person",
            },
            {
                "title": "Workshop: Build your first ML model with Python",
                "description": "4-hour hands-on workshop where you'll build a machine learning model from scratch using scikit-learn. Basic Python knowledge required. Very limited spots available.",
                "duration": "4h",
                "price": 15,
                "format": "In-person",
            },
            {
                "title": "Talk: The future of generative AI in business",
                "description": "Speakers from the tech and academic sectors will debate the impact of LLMs on business processes, AI regulation in Europe, and the job opportunities emerging from the ecosystem.",
                "duration": "2h",
                "price": 0,
                "format": "Hybrid",
            },
            {
                "title": "Cybersecurity: Capture The Flag (CTF)",
                "description": "Team-based cybersecurity competition with challenges in cryptography, reversing, web and forensics. Beginner and advanced categories available. Sponsored by Deloitte Cyber.",
                "duration": "6h",
                "price": 0,
                "format": "In-person",
            },
            {
                "title": "Demo Day: University Deeptech Startups",
                "description": "10 university deeptech projects present their progress to a panel of investors and mentors. Networking reception with drinks. Open to the entire Madrid university community.",
                "duration": "3h",
                "price": 0,
                "format": "In-person",
            },
            {
                "title": "Intro to Mobile App Development",
                "description": "Learn the fundamentals of Flutter and React Native in this weekend workshop. By the end you'll have built your first fully functional mobile app ready to publish.",
                "duration": "8h",
                "price": 25,
                "format": "In-person",
            },
        ]
    },
    "Entrepreneurship": {
        "emoji": "🚀",
        "color": "#e8ff47",
        "events": [
            {
                "title": "University Startup Weekend Madrid",
                "description": "54 hours to go from idea to prototype. Form a team with fellow students, validate your idea with real users, and pitch to investors on Sunday. Food included all three days.",
                "duration": "54h",
                "price": 20,
                "format": "In-person",
            },
            {
                "title": "Workshop: How to raise your first funding round",
                "description": "A Business Angel and a VC share their perspective on what they look for in university startups: metrics, team, pitch deck and timing. Live Q&A and feedback session.",
                "duration": "2h",
                "price": 0,
                "format": "Online",
            },
            {
                "title": "Elevator Pitch Competition",
                "description": "You have 90 seconds to convince the jury. The top 5 ideas will win access to the university accelerator and mentoring sessions with successful entrepreneurs.",
                "duration": "3h",
                "price": 0,
                "format": "In-person",
            },
            {
                "title": "Entrepreneurs Networking · Madrid",
                "description": "Monthly meetup of students and alumni with their own projects. Relaxed atmosphere with tapas and drinks. Each attendee gets 2 minutes to introduce themselves. Perfect for finding co-founders.",
                "duration": "2h",
                "price": 5,
                "format": "In-person",
            },
        ]
    },
    "Art & Culture": {
        "emoji": "🎨",
        "color": "#f472b6",
        "events": [
            {
                "title": "Exhibition: 'Digital Cracks' — Generative Art",
                "description": "Collective exhibition by 12 university artists exploring the intersection of code, data and visual expression. Interactive works that respond to the viewer's movement.",
                "duration": "5 days",
                "price": 0,
                "format": "In-person",
            },
            {
                "title": "University Short Film Festival",
                "description": "Screening of the 20 best short films produced by film students from across Spain. Post-screening discussion with directors and the professional jury. Live awards ceremony.",
                "duration": "4h",
                "price": 3,
                "format": "In-person",
            },
            {
                "title": "Screenprinting & Street Art Workshop",
                "description": "Learn manual screenprinting and stencil design techniques with guest urban artists. Materials are included and you'll take home the works you create.",
                "duration": "3h",
                "price": 12,
                "format": "In-person",
            },
            {
                "title": "Open Mic Night: Poetry & Spoken Word",
                "description": "A night of poetry, prose and poetic performance. Anyone can take the stage for 5 minutes. Intimate atmosphere, good vibes and fair-trade coffee.",
                "duration": "2.5h",
                "price": 0,
                "format": "In-person",
            },
        ]
    },
    "Science & Research": {
        "emoji": "🔬",
        "color": "#34d399",
        "events": [
            {
                "title": "European Researchers' Night",
                "description": "Over 40 researchers open their labs to the public. Live experiments ranging from particle physics to neuroscience. Activities for all levels, no prior knowledge required.",
                "duration": "5h",
                "price": 0,
                "format": "In-person",
            },
            {
                "title": "Madrid Young Researchers Congress",
                "description": "Scientific congress exclusively for undergraduate, master's and PhD students. Present your thesis project or research before a scientific committee. Certificates and prizes awarded.",
                "duration": "2 days",
                "price": 10,
                "format": "In-person",
            },
            {
                "title": "Workshop: Scientific Data Visualisation",
                "description": "Learn to communicate scientific results with modern tools: R, Python and Tableau. Practical case studies using real data from papers published in Nature and Science.",
                "duration": "4h",
                "price": 0,
                "format": "Online",
            },
            {
                "title": "Talk: University spin-offs with global impact",
                "description": "Founders of companies born in Madrid universities explain how they moved from the lab to the market. Sectors covered: biotech, cleantech, agritech and advanced materials.",
                "duration": "2h",
                "price": 0,
                "format": "Hybrid",
            },
        ]
    },
    "Sport & Wellness": {
        "emoji": "⚽",
        "color": "#fb923c",
        "events": [
            {
                "title": "Inter-Faculty Futsal Tournament",
                "description": "University futsal league with teams from all faculties. Matches on Wednesdays and Fridays over 6 weeks. Registered referees and live streaming included.",
                "duration": "6 weeks",
                "price": 5,
                "format": "In-person",
            },
            {
                "title": "Yoga & Meditation Weekend Retreat",
                "description": "Two days of total disconnection in the Madrid mountains. Yoga sessions, guided meditation, healthy food and academic stress management techniques. Very limited spots.",
                "duration": "2 days",
                "price": 45,
                "format": "In-person",
            },
            {
                "title": "Sierra de Guadarrama Hiking Trip",
                "description": "One-day excursion to the most iconic peaks of Guadarrama. Medium difficulty. Bus transport from universities included. Certified guide and insurance included.",
                "duration": "8h",
                "price": 18,
                "format": "In-person",
            },
            {
                "title": "Running Clinic: Improve your technique",
                "description": "Practical session with a certified coach. Biomechanical gait analysis, posture correction and personalised training plan. Includes video analysis.",
                "duration": "2h",
                "price": 10,
                "format": "In-person",
            },
        ]
    },
    "Sustainability": {
        "emoji": "🌱",
        "color": "#4ade80",
        "events": [
            {
                "title": "Green Campus: Sustainability Hackathon",
                "description": "Solve real sustainability challenges proposed by Madrid City Council and IBEX 35 companies. Cash prizes and the possibility of implementing the winning solution.",
                "duration": "24h",
                "price": 0,
                "format": "In-person",
            },
            {
                "title": "Debate: Can technology save the planet?",
                "description": "Oxford-format debate between academics, activists and business leaders on the role of technology in the climate crisis. Audience vote before and after the debate.",
                "duration": "2h",
                "price": 0,
                "format": "Hybrid",
            },
            {
                "title": "Composting & Urban Garden Workshop",
                "description": "Learn how to set up a home composting system and a garden in small spaces. The seed kit and composter are raffled among attendees.",
                "duration": "3h",
                "price": 8,
                "format": "In-person",
            },
        ]
    },
    "Languages & International": {
        "emoji": "🌍",
        "color": "#a78bfa",
        "events": [
            {
                "title": "Language Exchange Speed Dating",
                "description": "Practise your English, French, German or Mandarin with native-speaking students in quick 5-minute rounds. Fun and relaxed atmosphere. Over 200 participants expected.",
                "duration": "2h",
                "price": 0,
                "format": "In-person",
            },
            {
                "title": "Erasmus & International Programmes Fair",
                "description": "Representatives from over 50 European and American universities present their exchange programmes. Alumni students share their experience. Information sessions on scholarships.",
                "duration": "4h",
                "price": 0,
                "format": "In-person",
            },
            {
                "title": "Conference: Diplomacy & International Relations",
                "description": "Former diplomats and geopolitical analysts debate the new world order and career opportunities in international organisations such as the UN, EU and OECD.",
                "duration": "2.5h",
                "price": 0,
                "format": "Hybrid",
            },
        ]
    },
    "Law & Society": {
        "emoji": "⚖️",
        "color": "#fbbf24",
        "events": [
            {
                "title": "Moot Court: International Law Simulation",
                "description": "International law competition where student teams represent parties in a fictitious case before a panel of real magistrates. Preparatory phase included.",
                "duration": "3 days",
                "price": 0,
                "format": "In-person",
            },
            {
                "title": "Round Table: Digital Rights & Privacy",
                "description": "Digital law experts, privacy activists and representatives from the Spanish Data Protection Agency debate the future of GDPR and new AI challenges.",
                "duration": "2h",
                "price": 0,
                "format": "Online",
            },
            {
                "title": "Legal Clinic: Free advice for students",
                "description": "Law students supervised by professors offer free legal advice to the university community. Cases covered: rental, employment and consumer law.",
                "duration": "4h",
                "price": 0,
                "format": "In-person",
            },
        ]
    },
    "Music & Performances": {
        "emoji": "🎵",
        "color": "#60a5fa",
        "events": [
            {
                "title": "University Music Festival · Madrid",
                "description": "Three simultaneous stages with university bands and DJs all afternoon and evening. Genres: indie, electronic, jazz fusion and hip-hop. Craft beer included.",
                "duration": "8h",
                "price": 12,
                "format": "In-person",
            },
            {
                "title": "University Symphony Orchestra Concert",
                "description": "The orchestra of over 80 students performs works by Beethoven, Ravel and Piazzolla. Free entry until capacity is reached. Dress code: smart casual.",
                "duration": "2h",
                "price": 0,
                "format": "In-person",
            },
            {
                "title": "Open Mic: Singer-Songwriters & Music Production",
                "description": "An evening of performances by university singer-songwriters and producers showcasing their latest compositions. The audience votes for their favourite. Prize: professional studio recording.",
                "duration": "3h",
                "price": 3,
                "format": "In-person",
            },
        ]
    },
    "Mental Health & Psychology": {
        "emoji": "🧠",
        "color": "#c084fc",
        "events": [
            {
                "title": "Workshop: Managing Stress During Exam Season",
                "description": "Psychologists from the university counselling service share evidence-based techniques to manage anxiety, improve concentration and optimise sleep during exams.",
                "duration": "2h",
                "price": 0,
                "format": "In-person",
            },
            {
                "title": "University Mental Health Day",
                "description": "Talks, workshops and round tables on emotional wellbeing in the university environment. Psychiatrists, psychologists and students speak first-hand. Safe space guaranteed.",
                "duration": "6h",
                "price": 0,
                "format": "Hybrid",
            },
            {
                "title": "Support Group: Impostor Syndrome",
                "description": "Weekly space facilitated by psychologists to talk about impostor syndrome in academic life. Group dynamics and tools for self-compassion and confidence.",
                "duration": "1.5h",
                "price": 0,
                "format": "In-person",
            },
        ]
    },
}

# ─── VENUES BY UNIVERSITY ─────────────────────────────────────────────────────
VENUES = {
    "Universidad Complutense de Madrid": [
        "Main Auditorium - Law Faculty", "Paraninfo", "Government Pavilion",
        "Degree Room - Philology", "Complutense Cultural Centre", "María Zambrano Library"
    ],
    "Universidad Autónoma de Madrid": [
        "Pavilion C - Common Room", "Student Hub Space", "Module XIII Lecture Hall",
        "Higher Studies Centre", "Humanities Library"
    ],
    "Universidad Carlos III de Madrid": [
        "Room 14.0.08 - Padre Soler Building", "Leganés Auditorium",
        "Multi-purpose Room - Getafe Campus", "UC3M Innovation Centre"
    ],
    "Universidad Politécnica de Madrid": [
        "ETSI Telecomunicación - Main Hall", "Room B0 - ETSI Informáticos",
        "Technology Innovation Centre", "Architecture School Courtyard"
    ],
    "Universidad Rey Juan Carlos": [
        "Main Hall - Móstoles Campus", "Alcorcón Multi-purpose Room",
        "URJC Cultural Centre", "Vicálvaro Campus Library"
    ],
    "Universidad de Alcalá": [
        "San Ildefonso College", "Historic Paraninfo", "Sciences Lecture Hall",
        "UAH Botanical Garden"
    ],
    "Universidad Nebrija": [
        "Nebrija Cinema Room", "Innovation Hub", "Coworking Space - La Dehesa Campus"
    ],
    "Universidad Pontificia Comillas": [
        "ICAI Conference Room", "Alberto Aguilera Main Hall",
        "ICADE Business School Auditorium", "Rafael Mª de Hornedo Library"
    ],
    "IE University Madrid": [
        "IE Tower - Main Auditorium", "María de Molina Room", "Innovation Hub Floor 8"
    ],
    "Universidad Francisco de Vitoria": [
        "Pozuelo Campus Auditorium", "Sciences Multi-purpose Room", "UFV Entrepreneurship Hub"
    ],
}

# ─── ORGANISERS ───────────────────────────────────────────────────────────────
ORGANISERS = [
    "Student Council", "Computer Science Club", "Debate Society",
    "Student Scientific Society", "Entrepreneurs Club", "Cultural Committee",
    "Sports Association", "Theatre Group", "Green Brigade", "HR Department",
    "Alumni Network", "Technology Transfer Office", "Photography Club",
    "International Students Association", "Social Entrepreneurship Network"
]


def generate_events() -> pd.DataFrame:
    """Generate the full events database."""
    random.seed(42)
    now = datetime.now()
    events = []
    eid = 1000

    for uni_name in UNIVERSITIES:
        venues = VENUES.get(uni_name, ["Main Hall", "Auditorium"])
        for topic_name, topic_data in TOPICS.items():
            for ev_template in topic_data["events"]:
                # Distribute dates: ~30% this week, ~40% this month, ~30% this semester
                period_days = random.choices([7, 30, 120], weights=[30, 40, 30])[0]
                day_offset = random.randint(0, period_days)
                hour = random.choice([9, 10, 11, 12, 16, 17, 18, 19, 20])
                date = now + timedelta(days=day_offset, hours=hour, minutes=random.choice([0, 15, 30]))

                capacity = random.randint(30, 400)
                demand_boost = 1.3 if topic_name in ["Technology & AI", "Entrepreneurship", "Sport & Wellness"] else 1.0
                attendees = min(capacity, int(random.uniform(0.3, 0.98) * capacity * demand_boost))
                featured = (attendees / capacity > 0.75) and random.random() > 0.6

                event = {
                    "id": eid,
                    "title": ev_template["title"],
                    "description": ev_template["description"],
                    "university": uni_name,
                    "topic": topic_name,
                    "emoji": topic_data["emoji"],
                    "date": date,
                    "venue": random.choice(venues),
                    "format": ev_template["format"],
                    "duration": ev_template["duration"],
                    "price": ev_template["price"],
                    "capacity": capacity,
                    "attendees": attendees,
                    "organiser": random.choice(ORGANISERS),
                    "featured": featured,
                    "topic_color": topic_data["color"],
                }
                events.append(event)
                eid += 1

    df = pd.DataFrame(events)
    df["date"] = pd.to_datetime(df["date"])
    return df
