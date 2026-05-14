# Codex Skills: Installation, Management, and Usage Guide

This guide explains how to:
- Download Codex
- Sign in
- Create and install skills
- Upload custom skills
- Manage skills
- Use skills effectively

---

## Download Codex

Go to:

https://chatgpt.com/codex/

Codex is accessed through the ChatGPT platform (web or supported desktop environments).

![Codex Login](images/1-codex-landing.png)

After opening the page, click:

**Continue with ChatGPT**

---

## Sign In

![Codex Chat](images/2-codex-login.png)

Sign in using one of the following:
- Google
- Apple
- Microsoft
- Email
- Phone

After signing in, you will enter the Codex workspace.

HHS users can use their HHS email to sign in to access HHS-specific codex. 

---

## Codex Workspace

![Codex Chat](images/3-codex-chatting.png)

The workspace allows you to:
- Interact via chat
- Use plugins and skills
- Upload files
- Execute workflows

---

## Open the Plugins Panel

![Plugins Sidebar](images/6-codex-skill-plugin.png)

From the left sidebar:

- Click **Plugins**

This section contains:
- Skills
- Plugins
- Integrations


---

## Create a Skill

### Option A: Using the Interface

- Click **Manage**
- Click **Create**
- Select **Create skill**

![Plugins Sidebar](images/7-codex-skill-plugin-manage-skill.png)
---

### Option B: Using Command

![Trigger Skill Creation](images/4-codex-cli-create-skill.png)

In the chat input, enter: /skill create
This opens the Skill Creator.

---
## Upload a Skill Package

![Upload Skill ZIP](images/5-codex-attach-compressed-skill.png)

To install a custom skill:

- Drag and drop a `ccdi-federation-ai-copilot.zip` file into the chat
- Ensure **Skill Creator** is selected
- Submit the request

Codex will automatically:
- Parse the package
- Create the skill
- Register it in the system


## Using Skills

Skills are used directly within the Codex chat interface. There are several ways to invoke them.



### Explicit Invocation

![use skill](images/8-codex-use-skill.png)

You can explicitly direct Codex to use a specific skill. By typing the skill name, such as /ccdi-federation-ai-copilot, you can ensure that Codex uses that skill for your request.



![use skill2](images/9-codex-use-skill2.png)