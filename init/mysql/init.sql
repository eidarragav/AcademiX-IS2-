CREATE DATABASE IF NOT EXISTS academix_gateway;
CREATE DATABASE IF NOT EXISTS academix_courses;
CREATE DATABASE IF NOT EXISTS academix_evaluations;

GRANT ALL PRIVILEGES ON academix_gateway.* TO 'academix'@'%';
GRANT ALL PRIVILEGES ON academix_courses.* TO 'academix'@'%';
GRANT ALL PRIVILEGES ON academix_evaluations.* TO 'academix'@'%';

FLUSH PRIVILEGES;