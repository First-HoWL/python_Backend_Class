import { useState } from 'react';
import { Link } from 'react-router-dom';
import './Auth.scss';

export function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const set = k => e => setForm(p => ({ ...p, [k]: e.target.value }));

  return (
    <div className="auth">
      <div className="auth__card">
        <div className="auth__logo">Quiz<span>Hub</span></div>
        <h1>Вхід</h1>
        <p>Раді бачити вас знову</p>

        <div className="auth__form">
          <div className="auth__field">
            <label>Email</label>
            <input type="email" placeholder="you@example.com" value={form.email} onChange={set('email')} />
          </div>
          <div className="auth__field">
            <label>Пароль</label>
            <input type="password" placeholder="••••••••" value={form.password} onChange={set('password')} />
          </div>
          <button className="btn btn--primary auth__submit">Увійти</button>
        </div>

        <p className="auth__switch">
          Немає акаунту? <Link to="/register">Зареєструватись</Link>
        </p>
      </div>
    </div>
  );
}

export function Register() {
  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'student' });
  const set = k => e => setForm(p => ({ ...p, [k]: e.target.value }));

  return (
    <div className="auth">
      <div className="auth__card">
        <div className="auth__logo">Quiz<span>Hub</span></div>
        <h1>Реєстрація</h1>
        <p>Створіть акаунт безкоштовно</p>

        <div className="auth__form">
          <div className="auth__field">
            <label>Ім'я</label>
            <input type="text" placeholder="Ваше ім'я" value={form.name} onChange={set('name')} />
          </div>
          <div className="auth__field">
            <label>Email</label>
            <input type="email" placeholder="you@example.com" value={form.email} onChange={set('email')} />
          </div>
          <div className="auth__field">
            <label>Пароль</label>
            <input type="password" placeholder="Мінімум 8 символів" value={form.password} onChange={set('password')} />
          </div>
          <div className="auth__field">
            <label>Роль</label>
            <div className="auth__roles">
              {[['student', '🎓 Студент'], ['teacher', '👨‍🏫 Вчитель']].map(([val, lbl]) => (
                <button
                  key={val}
                  type="button"
                  className={`auth__role-btn ${form.role === val ? 'auth__role-btn--active' : ''}`}
                  onClick={() => setForm(p => ({ ...p, role: val }))}
                >
                  {lbl}
                </button>
              ))}
            </div>
          </div>
          <button className="btn btn--primary auth__submit">Зареєструватись</button>
        </div>

        <p className="auth__switch">
          Вже є акаунт? <Link to="/login">Увійти</Link>
        </p>
      </div>
    </div>
  );
}
