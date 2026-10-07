/**
 * CME396 Process Planning and Cost Estimation – MCQ Quiz (Units 1 to 4)
 *
 * HOW TO USE
 * 1. Open https://script.google.com and click "New project".
 * 2. Delete the sample code, paste this whole file, and click Save.
 * 3. Select the function "createQuiz" and click Run.
 * 4. Allow the permissions Google asks for (first time only).
 * 5. Open View > Logs (or Execution log): it shows the edit link and the
 *    link to send to students. The form also appears in your Google Drive.
 *
 * The form is a quiz: 40 questions, 1 mark each, answers and marks are set,
 * students see their score after submitting.
 */
const QUIZ_TITLE = "CME396 – Process Planning and Cost Estimation: MCQ Test (Units 1–4)";
const QUIZ_DESCRIPTION = "III Year / V Semester – Mechanical Engineering. 40 questions, 1 mark each. Choose the correct answer.";

const UNITS = [
 {
  "unit": "Unit 1 – Introduction to Process Planning",
  "qs": [
   {
    "q": "Process planning acts as the link between",
    "o": [
     "Finance and personnel",
     "Sales and marketing",
     "Purchase and stores",
     "Design and manufacturing"
    ],
    "a": 3
   },
   {
    "q": "In variant (retrieval) CAPP, the process plan for a new part is prepared by",
    "o": [
     "Trial and error on the shop floor",
     "Modifying the standard plan of a similar part family",
     "Creating the plan from scratch using decision logic",
     "Copying the plan of any random part"
    ],
    "a": 1
   },
   {
    "q": "Generative CAPP creates a process plan",
    "o": [
     "Only by editing an existing plan",
     "Without any computer",
     "From scratch using part data and decision logic",
     "Only for assembly operations"
    ],
    "a": 2
   },
   {
    "q": "Group technology arranges similar parts into",
    "o": [
     "Departments",
     "Bills of materials",
     "Part families",
     "Cost centres"
    ],
    "a": 2
   },
   {
    "q": "Which coding system is widely used for part classification in CAPP?",
    "o": [
     "Gantt code",
     "ISO 9001",
     "Opitz code",
     "Taylor code"
    ],
    "a": 2
   },
   {
    "q": "Which of the following is NOT an objective of process planning?",
    "o": [
     "Selecting the processes",
     "Deciding the sequence of operations",
     "Fixing the salary of workers",
     "Selecting machines and tools"
    ],
    "a": 2
   },
   {
    "q": "Manual process planning is most suitable for",
    "o": [
     "Small shops with low volume and few part types",
     "Fully automated factories",
     "Continuous process industries",
     "Mass production of thousands of part types"
    ],
    "a": 0
   },
   {
    "q": "On an engineering drawing, the surface finish (roughness) is usually specified by the value of",
    "o": [
     "Hardness in HRC",
     "Tolerance in degrees",
     "Density in g/cm³",
     "Ra in micrometres"
    ],
    "a": 3
   },
   {
    "q": "Material selection for a component is mainly based on",
    "o": [
     "Weight of the drawing sheet",
     "Name of the supplier only",
     "Function, properties, processability and cost",
     "Colour of the material only"
    ],
    "a": 2
   },
   {
    "q": "The process planning document that shows the sequence of departments / machines a part passes through is the",
    "o": [
     "Bill of materials",
     "Route sheet",
     "Purchase order",
     "Invoice"
    ],
    "a": 1
   }
  ]
 },
 {
  "unit": "Unit 2 – Process Planning Activities",
  "qs": [
   {
    "q": "Cutting speed in turning is given by (D in mm, N in rpm)",
    "o": [
     "V = DN / π m/min",
     "V = πDN / 1000 m/min",
     "V = 1000 / πDN m/min",
     "V = πD / N m/min"
    ],
    "a": 1
   },
   {
    "q": "A device that holds and locates the workpiece and also guides the cutting tool is called a",
    "o": [
     "Jig",
     "Mandrel",
     "Fixture",
     "Vice"
    ],
    "a": 0
   },
   {
    "q": "A device that holds and locates the workpiece but does NOT guide the tool is called a",
    "o": [
     "Template",
     "Fixture",
     "Jig",
     "Drill bush"
    ],
    "a": 1
   },
   {
    "q": "The 3-2-1 principle is used in jigs and fixtures for",
    "o": [
     "Coolant supply",
     "Clamping force calculation",
     "Tool sharpening",
     "Location of the workpiece"
    ],
    "a": 3
   },
   {
    "q": "How many locating points are used in the 3-2-1 principle?",
    "o": [
     "3",
     "12",
     "9",
     "6"
    ],
    "a": 3
   },
   {
    "q": "Break-even point is the level of production at which",
    "o": [
     "Total revenue equals total cost",
     "Variable cost is zero",
     "Fixed cost is zero",
     "Profit is maximum"
    ],
    "a": 0
   },
   {
    "q": "Break-even quantity is given by",
    "o": [
     "Selling price ÷ Fixed cost",
     "Fixed cost ÷ (Selling price per unit − Variable cost per unit)",
     "Variable cost ÷ Fixed cost",
     "(Fixed cost + Variable cost) ÷ Selling price"
    ],
    "a": 1
   },
   {
    "q": "The quality tool that plots process measurements against upper and lower control limits is the",
    "o": [
     "Route sheet",
     "Gantt chart",
     "Bill of materials",
     "Control chart"
    ],
    "a": 3
   },
   {
    "q": "The operation sheet gives details of",
    "o": [
     "Only the delivery date",
     "Only the selling price",
     "Each operation – machine, tools, speed, feed and time",
     "Only the raw material cost"
    ],
    "a": 2
   },
   {
    "q": "Increasing the feed in turning (other conditions same) will",
    "o": [
     "Have no effect on time",
     "Increase machining time and improve finish",
     "Reduce tool wear to zero",
     "Reduce machining time but increase surface roughness"
    ],
    "a": 3
   }
  ]
 },
 {
  "unit": "Unit 3 – Introduction to Cost Estimation",
  "qs": [
   {
    "q": "Estimation of the cost of a product is done",
    "o": [
     "Before production starts",
     "Only after production is completed",
     "Only by the cost accountant",
     "After the product is sold"
    ],
    "a": 0
   },
   {
    "q": "Prime cost is equal to",
    "o": [
     "Factory cost + Office overheads",
     "Direct material + Direct labour + Direct expenses",
     "Direct material + Overheads",
     "Total cost + Profit"
    ],
    "a": 1
   },
   {
    "q": "Factory cost is equal to",
    "o": [
     "Total cost − Selling overheads",
     "Direct material + Direct labour",
     "Prime cost + Factory overheads",
     "Prime cost + Profit"
    ],
    "a": 2
   },
   {
    "q": "Salary of the office staff is an example of",
    "o": [
     "Administrative overhead",
     "Factory overhead",
     "Direct labour",
     "Selling overhead"
    ],
    "a": 0
   },
   {
    "q": "Cost of lubricating oil and cotton waste used in a machine shop is",
    "o": [
     "Indirect material",
     "Direct material",
     "Selling overhead",
     "Direct expense"
    ],
    "a": 0
   },
   {
    "q": "A firm produces 600 machines a year with total overheads of Rs. 1,80,000. Overhead per machine by unit rate method is",
    "o": [
     "Rs. 180",
     "Rs. 3,000",
     "Rs. 600",
     "Rs. 300"
    ],
    "a": 3
   },
   {
    "q": "The most accurate method of allocating overheads in a machine shop is the",
    "o": [
     "Unit rate method",
     "Percentage of direct material method",
     "Machine hour rate method",
     "Percentage of prime cost method"
    ],
    "a": 2
   },
   {
    "q": "In the straight line method, the annual depreciation is",
    "o": [
     "C × n",
     "(C + S) / n",
     "(C − S) / n",
     "S / (C × n)"
    ],
    "a": 2
   },
   {
    "q": "Depreciation charged is highest in the early years of the asset's life in the",
    "o": [
     "Unit rate method",
     "Straight line method",
     "Machine hour method",
     "Reducing balance method"
    ],
    "a": 3
   },
   {
    "q": "The costing method suitable for cement, sugar and chemical industries is",
    "o": [
     "Process costing",
     "Operating costing",
     "Contract costing",
     "Job costing"
    ],
    "a": 0
   }
  ]
 },
 {
  "unit": "Unit 4 – Production Cost Estimation (Forging, Welding, Foundry)",
  "qs": [
   {
    "q": "In forging, the metal lost as iron oxide when the stock is heated is called",
    "o": [
     "Sprue loss",
     "Flash loss",
     "Scale loss",
     "Tonghold loss"
    ],
    "a": 2
   },
   {
    "q": "Scale loss in forging is generally taken as about",
    "o": [
     "0.5% of net weight",
     "50% of net weight",
     "25% of net weight",
     "6% of net weight"
    ],
    "a": 3
   },
   {
    "q": "The excess metal squeezed out between the die halves in closed-die forging is called",
    "o": [
     "Scale",
     "Sprue",
     "Burr",
     "Flash"
    ],
    "a": 3
   },
   {
    "q": "Gross weight of a forging is equal to",
    "o": [
     "Losses only",
     "Net weight × Density",
     "Net weight − Losses",
     "Net weight + Losses"
    ],
    "a": 3
   },
   {
    "q": "The pattern allowance provided to compensate for contraction of metal on cooling is",
    "o": [
     "Shake allowance",
     "Shrinkage allowance",
     "Draft allowance",
     "Machining allowance"
    ],
    "a": 1
   },
   {
    "q": "The taper given on the vertical faces of a pattern for easy withdrawal from the mould is",
    "o": [
     "Distortion allowance",
     "Shrinkage allowance",
     "Draft allowance",
     "Machining allowance"
    ],
    "a": 2
   },
   {
    "q": "Cross-sectional area of a single-V butt weld (thickness t, root gap g, included angle θ, no reinforcement) is",
    "o": [
     "g t + t² tan(θ/2)",
     "g t + t² sin θ",
     "g + t tan θ",
     "½ t²"
    ],
    "a": 0
   },
   {
    "q": "Operator factor in welding is the ratio of",
    "o": [
     "Arc time to total working time",
     "Total time to arc time",
     "Electrode used to weld deposited",
     "Voltage to current"
    ],
    "a": 0
   },
   {
    "q": "In foundry cost estimation, gates, runners and risers are",
    "o": [
     "Treated as direct labour",
     "Ignored completely",
     "Remelted as returns and credited at scrap value",
     "Added to the finished casting weight"
    ],
    "a": 2
   },
   {
    "q": "In soldering, the filler metal melts at a temperature",
    "o": [
     "Equal to the melting point of the base metal",
     "Above the melting point of steel",
     "Above 1500 °C",
     "Below 450 °C"
    ],
    "a": 3
   }
  ]
 }
];

function createQuiz() {
  const form = FormApp.create(QUIZ_TITLE);
  form.setDescription(QUIZ_DESCRIPTION);
  form.setIsQuiz(true);
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false);
  form.setShuffleQuestions(false);
  form.setProgressBar(true);

  form.addTextItem().setTitle("Name").setRequired(true);
  form.addTextItem().setTitle("Register Number").setRequired(true);

  UNITS.forEach(function (unit) {
    form.addPageBreakItem().setTitle(unit.unit);
    unit.qs.forEach(function (q, i) {
      const item = form.addMultipleChoiceItem();
      item.setTitle((i + 1) + ". " + q.q)
        .setChoices(q.o.map(function (opt, k) { return item.createChoice(opt, k === q.a); }))
        .setPoints(1)
        .setRequired(true);
    });
  });

  Logger.log("Edit the form:    " + form.getEditUrl());
  Logger.log("Send to students: " + form.getPublishedUrl());
}
