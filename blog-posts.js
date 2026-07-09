// Add new posts to this array. Fields used by the homepage:
// slug, title, date, category, project, summary, tags, color, featured, body, url.
// Use body for in-page posts, or url for an external article/project page.
window.neuraPosts = [
    {
        slug: "shared-infrastructure-as-research-output",
        title: "Shared infrastructure as a research output",
        date: "2026-07-09",
        category: "Essay",
        project: "Project Neura",
        summary: "Why the systems around experiments, handoffs, and reproducibility should be treated as durable research work rather than background setup.",
        tags: ["infrastructure", "community", "reproducibility"],
        color: "#d54b3d",
        featured: true,
        body: [
            "Project Neura is built around a simple premise: the tooling around research is part of the research. If an experiment can only be repeated by the person who happened to set it up, the work is weaker than it needs to be.",
            "The organization is shaped to turn repeated setup into shared infrastructure. That includes project templates, compute conventions, writing habits, and the interfaces between researchers and developers.",
            "The goal is not to make every project identical. It is to let each project inherit enough structure that contributors can spend more of their time on the actual problem."
        ]
    },
    {
        slug: "erbium-compute-layer-note",
        title: "Erbium and the compute layer beneath the gallery",
        date: "2026-06-18",
        category: "Project Note",
        project: "Erbium",
        summary: "A short note on treating orchestration, execution, and repeatable workflows as a shared backbone for Neura projects.",
        tags: ["compute", "orchestration", "systems"],
        color: "#1f5f9f",
        body: [
            "Erbium is the infrastructure-facing side of Project Neura: the place where repeatable execution patterns and operational conventions become reusable.",
            "A shared compute layer matters because it lets project teams carry lessons forward. When setup, logging, and environment conventions are consistent, experiments become easier to inspect and easier to improve.",
            "Future posts can use this same format for release notes, design notes, or implementation reports."
        ]
    },
    {
        slug: "segwithu-segmentation-uncertainty",
        title: "SegWithU and segmentation uncertainty",
        date: "2026-06-04",
        category: "Research Note",
        project: "SegWithU",
        summary: "A research note on SegWithU as a segmentation uncertainty project for estimating, analyzing, and using uncertainty in visual prediction workflows.",
        tags: ["uncertainty", "segmentation", "vision"],
        color: "#5b6f9f",
        body: [
            "SegWithU belongs in the research gallery as a project focused on uncertainty in segmentation. The core question is not only what a model predicts, but how confidently and reliably that prediction should be interpreted.",
            "Uncertainty work benefits from the same Neura structure as infrastructure projects: clear experiment records, repeatable evaluation, and notes that preserve the choices behind each iteration.",
            "As SegWithU develops, this notebook can hold dataset notes, uncertainty methods, model comparisons, and short reports from each research milestone."
        ]
    },
    {
        slug: "mip-candy-research-setup",
        title: "Packaging experiment setup into MIP Candy",
        date: "2026-05-27",
        category: "Release",
        project: "MIP Candy",
        summary: "MIP Candy turns a complete PyTorch experiment scaffold into a reusable starting point for faster research iteration.",
        tags: ["PyTorch", "templates", "experiments"],
        color: "#357761",
        body: [
            "MIP Candy exists to reduce the blank-page cost of starting a serious machine learning experiment. Instead of rebuilding the same pipeline shape again, contributors can begin from a working scaffold.",
            "The project reflects a broader Neura pattern: once a team solves a recurring setup problem, package it so the next team starts from that solution.",
            "That makes the first experiment faster, but the larger value is continuity. Results, configs, and code organization become easier to compare across efforts."
        ]
    },
    {
        slug: "leads-interface-thinking",
        title: "Interface thinking in LEADS",
        date: "2026-04-12",
        category: "Field Note",
        project: "LEADS",
        summary: "LEADS is an applied project surface where telemetry, control, and analysis benefit from the same interface discipline used across Neura.",
        tags: ["interfaces", "telemetry", "applied"],
        color: "#b7772a",
        body: [
            "Applied systems need clear interfaces because messy boundaries slow every later decision. LEADS gives Project Neura a place to apply that discipline to telemetry, control, and analysis.",
            "The same habits that help research infrastructure also help applied work: explicit data contracts, repeatable workflows, and documentation that explains why a choice was made.",
            "As the gallery grows, project notes like this can connect public milestones to the engineering patterns behind them."
        ]
    }
];
