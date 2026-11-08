-- Диагностика PostgreSQL для скриншотов и проверки ПК 4.1/4.2
SELECT current_database(), current_user, version();
SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;
SELECT * FROM users ORDER BY id;
SELECT * FROM software_components ORDER BY id;
SELECT * FROM service_tickets ORDER BY id;
SELECT * FROM audit_logs ORDER BY id DESC LIMIT 20;
