# Somata Blender Plugin

Generate and import photorealistic digital human meshes from inside Blender via the [Somata](https://github.com/3pda/SomataFrontEnd) API.

## Features

- **Upload Reference Photo** — upload a JPEG/PNG with name, gender, height, and weight; generates a mesh from a real likeness
- **Import Mesh** — download a READY asset's FBX directly into the current scene
- **My Assets** — browse your asset library from the N-panel; refresh on demand

## Requirements

- Blender 3.3 LTS or later
- A Somata account ([sign up at /early-access](https://somata.ai/early-access))

## Installation

### From release zip (recommended)

1. Download `somata_blender-X.Y.Z.zip` from [Releases](https://github.com/3pda/somata-blender/releases)
2. In Blender: **Edit → Preferences → Add-ons → Install…**
3. Select the zip → enable **Somata**

### From source

```bash
git clone https://github.com/3pda/somata-blender
cd somata-blender
make zip
# Then install the generated zip via Blender Preferences
```

## Setup

1. Open **Edit → Preferences → Add-ons → Somata**
2. Set your **API URL** (default: `http://localhost:3001` for local dev; set to your hosted URL for production)
3. In the **Somata** N-panel (3D Viewport → Sidebar → Somata), click **Log In**

## Usage

### Upload a photo
1. In the **Somata** panel, fill in **Name**, **Gender**, **Height (cm)**, and **Weight (kg)**
2. Click **Pick Photo…** and select a JPEG/PNG reference image
3. The mesh generates in the background — check **My Assets** for status

### Import a mesh
1. In **My Assets**, click **Refresh** (or **Load Assets**) to fetch your library
2. Once an asset shows **READY**, click the **Import** button next to it
3. The FBX is downloaded and imported into the current scene

## Development

```bash
# No external dependencies — uses Python stdlib only (urllib)
# Run Blender with the addon loaded from source:
blender --python-expr "import bpy; bpy.ops.preferences.addon_install(filepath='.')"
```

## No external dependencies

The plugin uses only Python stdlib (`urllib`, `json`, `threading`) — no `pip install` required. Blender's bundled Python is all you need.
