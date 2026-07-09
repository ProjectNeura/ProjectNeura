// Add new projects to this array. Fields used by the homepage:
// name, code, category, color, summary, tags, url.
// Supported current categories: research, systems, tools, applied.
// If url is omitted, the card still appears and shows a category label instead of a link.
window.neuraProjects = [
    {
        name: "SegWithU",
        code: "Research project",
        category: "research",
        color: "#5b6f9f",
        url: "https://github.com/ProjectNeura/SegWithU",
        summary: "A segmentation uncertainty research project for estimating, analyzing, and working with model uncertainty in visual prediction workflows.",
        tags: ["uncertainty", "segmentation", "vision"]
    },
    {
        name: "LEADS",
        code: "Applied system",
        category: "applied",
        color: "#d54b3d",
        url: "https://leads.projectneura.org",
        summary: "Telemetry, control, and analysis for high-performance systems, built on shared engineering patterns and reusable operational infrastructure.",
        tags: ["vehicle intelligence", "interfaces", "analysis"]
    },
    {
        name: "Erbium",
        code: "Core backbone",
        category: "systems",
        color: "#1f5f9f",
        url: "https://erbium.projectneura.org",
        summary: "A modular compute and orchestration layer for repeatable workflows, shared execution, and project infrastructure reuse.",
        tags: ["compute", "orchestration", "reproducibility"]
    },
    {
        name: "MIP Candy",
        code: "Research tool",
        category: "tools",
        color: "#357761",
        url: "https://mipcandy.projectneura.org",
        summary: "Fast setup for complete PyTorch MIP experiment pipelines, packaging hard-won experiment knowledge into a reusable starting point.",
        tags: ["PyTorch", "experiments", "templates"]
    }
];
