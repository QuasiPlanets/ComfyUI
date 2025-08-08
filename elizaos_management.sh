#!/bin/bash
# ElizaOS Management Script
# Provides quick commands for managing the ElizaOS real-time transcription system

echo "🎤 ElizaOS Management Script"
echo "=========================="

case "$1" in
    "start")
        echo "🚀 Starting ElizaOS WebSocket Server..."
        cd /workspace
        python start_websocket_server.py &
        echo "✅ Server started in background"
        ;;
    "stop")
        echo "🛑 Stopping ElizaOS WebSocket Server..."
        pkill -f "start_websocket_server.py"
        echo "✅ Server stopped"
        ;;
    "status")
        echo "📊 ElizaOS System Status:"
        echo "ComfyUI Server:"
        netstat -tlnp | grep 8188 || echo "❌ Not running"
        echo "WebSocket Server:"
        netstat -tlnp | grep 8189 || echo "❌ Not running"
        ;;
    "test")
        echo "🧪 Testing ElizaOS Components..."
        cd /workspace/custom_nodes/ComfyUI-WhisperX
        python test_websocket_connection.py
        ;;
    "restart")
        echo "🔄 Restarting ElizaOS..."
        $0 stop
        sleep 2
        $0 start
        ;;
    "logs")
        echo "📋 Recent ElizaOS Logs:"
        tail -n 20 /workspace/server.log
        ;;
    *)
        echo "Usage: $0 {start|stop|status|test|restart|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start WebSocket server"
        echo "  stop    - Stop WebSocket server"
        echo "  status  - Check system status"
        echo "  test    - Test WebSocket connection"
        echo "  restart - Restart the system"
        echo "  logs    - Show recent logs"
        ;;
esac 