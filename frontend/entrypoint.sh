#!/bin/sh
echo "Starting frontend server"
npm install
echo "Running in local environment on port $FRONTEND_PORT"
npm run dev -- --port $FRONTEND_PORT --host