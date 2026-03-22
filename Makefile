ADDON_NAME = somata_blender
VERSION     = $(shell python3 -c "import ast, sys; bl_info = ast.literal_eval(open('__init__.py').read().split('bl_info = ')[1].split('\n\n')[0]); print('.'.join(map(str, bl_info['version'])))")
ZIP_NAME    = $(ADDON_NAME)-$(VERSION).zip

.PHONY: zip install clean

## Build a distributable .zip (drag-and-drop into Blender)
zip:
	rm -f $(ZIP_NAME)
	zip -r $(ZIP_NAME) . \
		--exclude "*.git*" \
		--exclude "__pycache__/*" \
		--exclude "*.pyc" \
		--exclude "*.DS_Store" \
		--exclude "$(ADDON_NAME)-*.zip" \
		--exclude "Makefile" \
		--exclude "*.md" \
		-x "*.json"
	@echo "Built: $(ZIP_NAME)"

## Install directly into Blender's addons directory (macOS default path)
install: zip
	cp $(ZIP_NAME) ~/Library/Application\ Support/Blender/4.2/extensions/user_default/
	@echo "Installed to Blender extensions directory"

clean:
	rm -f *.zip
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
