import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { postApiJson, saveSession } from '../../api';
import './Auth.scss';

export function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ login: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const set = k => e => setForm(p => ({ ...p, [k]: e.target.value }));

  const submit = async () => {
    if (!form.login || !form.password) {
      setError('Будь ласка, введіть логін і пароль.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const data = await postApiJson('/api/auth', {
        login: form.login,
        password: form.password,
      });
      saveSession(data);
      navigate('/');
    } catch (err) {
      setError(err.message || 'Помилка входу');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth">
      <div className="auth__card">
        <div className="auth__logo">Quiz<span>Hub</span></div>
        <h1>Вхід</h1>
        <p>Раді бачити вас знову</p>
        <div className="auth__form">
          <div className="auth__field">
            <label>Логін</label>
            <input type="text" placeholder="your_login" value={form.login} onChange={set('login')} />
          </div>
          <div className="auth__field">
            <label>Пароль</label>
            <input type="password" placeholder="••••••••" value={form.password} onChange={set('password')} />
          </div>
          {error && <p className="auth__error">{error}</p>}
          <button className="btn btn--primary auth__submit" onClick={submit} disabled={loading}>
            {loading ? 'Завантаження...' : 'Увійти'}
          </button>
        </div>
        <p className="auth__switch">
          Немає акаунту? <Link to="/register">Зареєструватись</Link>
        </p>
      </div>
    </div>
  );
}

export function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: '', login: '', password: '', isTeacher: false });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const set = k => e => setForm(p => ({ ...p, [k]: e.target.value }));

  const submit = async () => {
    if (!form.name || !form.login || !form.password) {
      setError('Будь ласка, заповніть усі поля.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      await postApiJson('/api/signin', {
        login: form.login,
        password: form.password,
        name: form.name,
        isTeacher: form.isTeacher,
      });
      const auth = await postApiJson('/api/auth', {
        login: form.login,
        password: form.password,
      });
      saveSession(auth);
      navigate('/');
    } catch (err) {
      setError(err.message || 'Помилка реєстрації');
    } finally {
      setLoading(false);
    }
  };

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
            <label>Логін</label>
            <input type="text" placeholder="your_login" value={form.login} onChange={set('login')} />
          </div>
          <div className="auth__field">
            <label>Пароль</label>
            <input type="password" placeholder="Мінімум 6 символів" value={form.password} onChange={set('password')} />
          </div>
          <div className="auth__field">
            <label>Роль</label>
            <div className="auth__roles">
              {[[false, '🎓 Студент'], [true, '👨‍🏫 Вчитель']].map(([val, lbl]) => (
                <button
                  key={String(val)}
                  type="button"
                  className={`auth__role-btn ${form.isTeacher === val ? 'auth__role-btn--active' : ''}`}
                  onClick={() => setForm(p => ({ ...p, isTeacher: val }))}
                >
                  {lbl}
                </button>
              ))}
            </div>
          </div>
          {error && <p className="auth__error">{error}</p>}
          <button className="btn btn--primary auth__submit" onClick={submit} disabled={loading}>
            {loading ? 'Завантаження...' : 'Зареєструватись'}
          </button>
        </div>
        <p className="auth__switch">
          Вже є акаунт? <Link to="/login">Увійти</Link>
        </p>
      </div>
    </div>
  );
}