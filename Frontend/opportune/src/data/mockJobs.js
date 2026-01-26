export const mockJobs = [
  {
    id: 1,
    title: "Senior Frontend Developer",
    company: "TechCorp Inc.",
    location: "San Francisco, CA",
    skills: ["React", "TypeScript", "CSS", "REST APIs"],
    matchScore: 95,
    description: "Looking for an experienced frontend developer to join our growing team.",
    salary: "$120k - $160k",
    type: "Full-time"
  },
  {
    id: 2,
    title: "Full Stack Engineer",
    company: "StartupXYZ",
    location: "Remote",
    skills: ["React", "Node.js", "MongoDB", "AWS"],
    matchScore: 88,
    description: "Build scalable web applications in a fast-paced startup environment.",
    salary: "$100k - $140k",
    type: "Full-time"
  },
  {
    id: 3,
    title: "UI/UX Developer",
    company: "Design Studios",
    location: "New York, NY",
    skills: ["React", "Figma", "CSS", "JavaScript"],
    matchScore: 82,
    description: "Create beautiful user interfaces and exceptional user experiences.",
    salary: "$90k - $130k",
    type: "Full-time"
  },
  {
    id: 4,
    title: "React Native Developer",
    company: "Mobile First Co.",
    location: "Austin, TX",
    skills: ["React Native", "JavaScript", "iOS", "Android"],
    matchScore: 78,
    description: "Develop cross-platform mobile applications for millions of users.",
    salary: "$110k - $150k",
    type: "Full-time"
  }
];

export const mockCourses = [
  {
    id: 1,
    title: "Advanced TypeScript Patterns",
    skill: "TypeScript",
    platform: "Udemy",
    difficulty: "Advanced",
    duration: "12 hours",
    rating: 4.8
  },
  {
    id: 2,
    title: "System Design for Interviews",
    skill: "System Design",
    platform: "Coursera",
    difficulty: "Intermediate",
    duration: "6 weeks",
    rating: 4.9
  },
  {
    id: 3,
    title: "AWS Solutions Architect",
    skill: "Cloud Computing",
    platform: "AWS Training",
    difficulty: "Intermediate",
    duration: "20 hours",
    rating: 4.7
  },
  {
    id: 4,
    title: "Modern CSS & Responsive Design",
    skill: "CSS",
    platform: "Frontend Masters",
    difficulty: "Beginner",
    duration: "8 hours",
    rating: 4.6
  }
];

export const interviewQuestions = {
  technical: [
    "Explain the virtual DOM and how React uses it for optimization",
    "What are React hooks and how do they differ from class lifecycle methods?",
    "Describe the difference between controlled and uncontrolled components",
    "How would you optimize a React application's performance?",
    "Explain closure in JavaScript with practical examples"
  ],
  behavioral: [
    "Tell me about a time you had to debug a complex issue",
    "Describe a situation where you had to work with a difficult team member",
    "How do you prioritize tasks when working on multiple projects?",
    "Tell me about a project you're most proud of",
    "How do you stay updated with new technologies?"
  ],
  common: [
    "Why do you want to work for our company?",
    "Where do you see yourself in 5 years?",
    "What are your salary expectations?",
    "What is your greatest strength and weakness?",
    "Why are you leaving your current position?"
  ]
};
