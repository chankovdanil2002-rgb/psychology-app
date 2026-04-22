import { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { FiMenu, FiX, FiUser, FiLogOut } from 'react-icons/fi';
import { useAuth } from '../../context/AuthContext';
import styles from './Header.module.css';

export default function Header() {
  const { isAuthenticated, isClient, isPsychologist, isAdmin, logout } =
    useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => setMenuOpen((prev) => !prev);
  const closeMenu = () => setMenuOpen(false);

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        {/* Logo */}
        <Link to="/" className={styles.logo} onClick={closeMenu}>
          Психологи института
        </Link>

        {/* Hamburger toggle (mobile) */}
        <button
          className={styles.hamburger}
          onClick={toggleMenu}
          aria-label={menuOpen ? 'Close menu' : 'Open menu'}
        >
          {menuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
        </button>

        {/* Navigation */}
        <nav className={`${styles.nav} ${menuOpen ? styles.navOpen : ''}`}>
          <NavLink
            to="/"
            className={({ isActive }) =>
              `${styles.navLink} ${isActive ? styles.active : ''}`
            }
            onClick={closeMenu}
          >
            Главная
          </NavLink>

          <NavLink
            to="/catalog"
            className={({ isActive }) =>
              `${styles.navLink} ${isActive ? styles.active : ''}`
            }
            onClick={closeMenu}
          >
            Психологи
          </NavLink>

          {isAuthenticated && isClient && (
            <NavLink
              to="/appointments"
              className={({ isActive }) =>
                `${styles.navLink} ${isActive ? styles.active : ''}`
              }
              onClick={closeMenu}
            >
              Мои записи
            </NavLink>
          )}

          {isAuthenticated && isPsychologist && (
            <NavLink
              to="/dashboard"
              className={({ isActive }) =>
                `${styles.navLink} ${isActive ? styles.active : ''}`
              }
              onClick={closeMenu}
            >
              Кабинет психолога
            </NavLink>
          )}

          {isAuthenticated && isAdmin && (
            <NavLink
              to="/admin/psychologists"
              className={({ isActive }) =>
                `${styles.navLink} ${isActive ? styles.active : ''}`
              }
              onClick={closeMenu}
            >
              Команда
            </NavLink>
          )}

          {/* Auth section */}
          {isAuthenticated ? (
            <div className={styles.authSection}>
              {/* Profile link */}
              <NavLink
                to="/profile"
                className={({ isActive }) =>
                  `${styles.navLink} ${styles.profileLink} ${isActive ? styles.active : ''}`
                }
                onClick={closeMenu}
              >
                <FiUser size={16} />
                <span>Личный кабинет</span>
              </NavLink>

              {/* Logout */}
              <button className={styles.logoutBtn} onClick={() => { logout(); closeMenu(); }}>
                <FiLogOut size={16} />
                <span>Выйти</span>
              </button>
            </div>
          ) : (
            <div className={styles.authSection}>
              <NavLink
                to="/login"
                className={({ isActive }) =>
                  `${styles.navLink} ${isActive ? styles.active : ''}`
                }
                onClick={closeMenu}
              >
                Войти
              </NavLink>
              <NavLink
                to="/register"
                className={`${styles.navLink} ${styles.registerBtn}`}
                onClick={closeMenu}
              >
                Регистрация
              </NavLink>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
}
