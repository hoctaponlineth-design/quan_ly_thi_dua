import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager # BỔ SUNG: Import thư viện quản lý context

# Đảm bảo thư mục data tồn tại
os.makedirs('data', exist_ok=True)

DB_URL = "sqlite:///data/thi_dua.db"

# Khởi tạo engine, check_same_thread=False cần thiết cho PySide6/GUI
engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_session():
    """Hàm cung cấp session để tương tác với DB (Giữ lại cho tương thích ngược)"""
    return SessionLocal()

# ==========================================
# BỔ SUNG MỚI: QUẢN LÝ SESSION THÔNG MINH
# ==========================================
@contextmanager
def session_scope():
    """Cung cấp một scope giao dịch an toàn cho các thao tác CSDL."""
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def seed_violation_categories():
    """Tự động thêm một số lỗi vi phạm mẫu nếu ngân hàng lỗi đang trống"""
    from database.models import ViolationCategory
    
    try:
        # ÁP DỤNG SESSION_SCOPE: Tự động quản lý commit/rollback/close
        with session_scope() as session:
            if session.query(ViolationCategory).count() == 0:
                sample_errors = [
                    ViolationCategory(name="Đi học muộn", penalty_points=2.0),
                    ViolationCategory(name="Sai đồng phục", penalty_points=1.0),
                    ViolationCategory(name="Vắng không phép", penalty_points=5.0),
                    ViolationCategory(name="Mất trật tự", penalty_points=2.0)
                ]
                session.add_all(sample_errors)
    except Exception as e:
        print(f"Lỗi mồi dữ liệu ngân hàng lỗi: {e}")

def init_db():
    """Tạo tất cả các bảng nếu chưa có"""
    from database.models import Base, ViolationCategory, WeeklyViolation 
    Base.metadata.create_all(bind=engine)
    
    # Gọi hàm mồi dữ liệu ngay sau khi tạo bảng
    seed_violation_categories()