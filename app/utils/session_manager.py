from datetime import datetime, timedelta
from .database import db
import uuid

class SessionManager:
    def __init__(self, expire_minutes=30):
        self.sessions = {}  # uuid -> (timestamp, is_admin)
        #  db.get("sessions",{})
        self.expire_minutes = expire_minutes

    def create_session(self, is_admin=True):
        """创建新会话并返回session_id"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = (datetime.now(), is_admin)
        return session_id

    def validate_session(self, session_id):
        """验证会话是否有效"""
        if not session_id or session_id not in self.sessions:
            return False
        
        timestamp, is_admin = self.sessions[session_id]
        if datetime.now() - timestamp > timedelta(minutes=self.expire_minutes):
            del self.sessions[session_id]
            return False
            
        # 更新时间戳
        self.sessions[session_id] = (datetime.now(), is_admin)
        return True

    def clear_expired(self):
        """清理过期会话"""
        current_time = datetime.now()
        expired = [
            sid for sid, (timestamp, _) in self.sessions.items()
            if current_time - timestamp > timedelta(minutes=self.expire_minutes)
        ]
        for sid in expired:
            del self.sessions[sid]