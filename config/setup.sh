#!/bin/bash

CONFIG_PATH="config"

# Copy environment configuration
cp -f "$CONFIG_PATH/.env.example" "$CONFIG_PATH/.env"

# Copy database initialization configuration
cp -f "$CONFIG_PATH/database.init.example" "$CONFIG_PATH/database.init"
