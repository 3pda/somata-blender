# Somata Blender Plugin

Generate and import photorealistic digital human meshes from inside Blender via the [Somata](https://github.com/3pda/SomataFrontEnd) API.

## Features

- **Upload Reference Photo** — upload a JPEG/PNG and generate a mesh from a real likeness
- **Generate from Measurements** — specify gender, height, and weight; get a free A-pose preview, then confirm to generate the full FBX (costs 1 credit)
- **Import Mesh** — download a READY asset's FBX directly into the current scene
- **My Assets** — browse your asset library from the N-panel

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
1. Click **Upload Reference Photo** in the Somata panel
2. Select a JPEG/PNG file, enter name + measurements
3. The mesh generates in the background — check **My Assets** for status

### Generate from measurements
1. Click **Generate Preview** — free, no credit used
2. Review the preview URL, then click **Generate Mesh (1 credit)**
3. Once READY, click **Import Mesh** in **My Assets**

## Development

```bash
# No external dependencies — uses Python stdlib only (urllib)
# Run Blender with the addon loaded from source:
blender --python-expr "import bpy; bpy.ops.preferences.addon_install(filepath='.')"
```

## No external dependencies

The plugin uses only Python stdlib (`urllib`, `json`, `threading`) — no `pip install` required. Blender's bundled Python is all you need.
