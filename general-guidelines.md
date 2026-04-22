# Project Neura General Guidelines

You can find the source code of this Markdown file [here](https://projectneura.org/general-guidelines.md).

## File Storage

You may have realized that there are many file storage solutions available. In this section, we will discuss the ones we
use at Project Neura and when to use which.

### Google Drive

This is probably the most common platform. You can simply register a Google account with your Project Neura email and
start using it. By default, you will get 15 GB of storage.

Google Drive is a great tool for quick sharing. However, due to the limited space and the fact that files cannot be
easily downloaded from Google Drive to Linux servers, it is only used for sending small-to-medium-size files through
Slack or Discord.

### Hugging Face

Similar to Google Drive, you can register a Hugging Face account with your Project Neura email and start using it. By
default, you will get 100 GB private storage and a lot of public storage.

You can use this whenever you want during the project.

### Central Data Storage Server

Project Neura's Central Data Storage (CDS) server, which is https://cds.projectneura.org, is an AWS S3-compatible
storage server. It has theoretically unlimited storage. One advantage of this server is that files on it can be
downloaded using `wget` at a high speed.

Members do not have write access to this server. At the end of each project, you must share all essential files with
your supervisor, and the supervisor must upload them to the CDS server. By default, files on CDS are public. They can be
made private by Cloudflare Access.

### Erbium Storage

[Erbium](https://erbium.projectneura.org) provides a node just for storage. It has 4 TB of storage, but the availability
is not guaranteed. One advantage of it is that files are backed up automatically.

It is the best option for sharing and storing files internally during the project. However, do keep in mind that all
members of Project Neura have access to it. For projects that are confidential and sensitive (most often due to
conflicts of interest), avoid using the Erbium storage and use Google Drive or Hugging Face instead.

## Computational Resources

We host private clusters using [Erbium](https://erbium.projectneura.org). Members can host their own nodes by installing
the [Erbium codebase](https://github.com/ProjectNeura/Erbium). In addition, we rent GPUs on [Vast.ai](https://vast.ai).
Upon registration, we will invite you to our organization account on Vast.ai and you can access all our GPUs.

## Best Practices

Generally, our infrastructures like [MIP Candy](https://mipcandy.projectneura.org) will force you to follow some
best practices. However, in some research topics where we currently do not have a dedicated pipeline yet, you shall
follow the following guidelines.

### Files

You must never delete files that are referenced or used by other team members or modules in the project.

Often, there are functions that create files and folders. Whenever you write code to do so, you should always check for
the existence of the file or directory before creating it, avoiding overwriting existing files unless you are
intentionally modifying them. One example is, if your code needs to save some sort of results to a file, running it
twice must generate two distinct files instead of overwriting the first one, but you may edit the file within one run.

If you are creating a new file, you should name it informatively. Some elements to consider are:
- The project name
- The module name
- The purpose of the file
- The date of creation
- The changes you made (change log)
- The version of the code
- The version of the file