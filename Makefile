DATA_DIR=data

.PHONY:
	clean

# Delete all data files except gitkeep
clean:
	find $(DATA_DIR) \! -name '.gitkeep' -delete