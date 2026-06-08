import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getApiJson, getStoredAccaunt, saveSession, API_BASE } from '../../api';
import './Profile.scss';

export default function Profile() {
  const navigate = useNavigate();
  const [accaunt, setAccaunt] = useState(null);
  const [tests, setTests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);
  const [profileForm, setProfileForm] = useState({ login: '', name: '', isTeacher: false });
  const [profileMessage, setProfileMessage] = useState('');
  const [savingProfile, setSavingProfile] = useState(false);

  useEffect(() => {
    const stored = getStoredAccaunt();
    if (!stored?.accaunt) { navigate('/login'); return; }
    setAccaunt(stored.accaunt);
    setProfileForm({ login: stored.accaunt.login, name: stored.accaunt.name, isTeacher: !!stored.accaunt.isTeacher });

    getApiJson('/api/tests')
      .then(data => setTests(data || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [navigate]);

  const saveProfile = async () => {
    setProfileMessage('');
    setSavingProfile(true);

    const stored = getStoredAccaunt();
    if (!stored?.access) {
      navigate('/login');
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/api/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
          Authorization: `Bearer ${stored.access}`,
        },
        body: JSON.stringify({
          login: profileForm.login,
          name: profileForm.name,
          isTeacher: profileForm.isTeacher,
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || data.detail || 'Не вдалося зберегти профіль');
      }

      const updatedSession = saveSession({
        access: stored.access,
        refresh: stored.refresh,
        accaunt: {
          ...stored.accaunt,
          login: data.login,
          name: data.name,
          isTeacher: data.isTeacher,
        },
      });
      setAccaunt(updatedSession.accaunt);
      setEditMode(false);
      setProfileMessage('Профіль успішно оновлено');
      setProfileForm(p => ({ ...p }));
    } catch (err) {
      setProfileMessage(err.message || 'Не вдалося зберегти профіль');
    } finally {
      setSavingProfile(false);
    }
  };

  if (!accaunt) return null;

  const initials = accaunt.name
    ?.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2) || '??';

  // Тесты созданные этим пользователем (если учитель)
  const myTests = tests.filter(t => t.author?.id === accaunt.id);

  return (
    <div className="profile">
      <div className="container">
        <div className="profile__hero">
          <div className="profile__avatar">{initials}</div>
          <div className="profile__info">
            <h1>{accaunt.name}</h1>
            <p>@{accaunt.login}</p>
            <span className="profile__role">{accaunt.isTeacher ? 'Вчитель' : 'Студент'}</span>
          </div>
          <button
            className="btn btn--outline profile__edit-btn"
            onClick={() => {
              setEditMode(o => !o);
              setProfileMessage('');
            }}
          >
            {editMode ? 'Скасувати' : 'Редагувати профіль'}
          </button>
        </div>

        {editMode && (
          <div className="profile__edit-panel">
            <div className="profile__form-row">
              <label>Логін</label>
              <input
                type="text"
                value={profileForm.login}
                onChange={e => setProfileForm(p => ({ ...p, login: e.target.value }))}
              />
            </div>
            <div className="profile__form-row">
              <label>Ім'я</label>
              <input
                type="text"
                value={profileForm.name}
                onChange={e => setProfileForm(p => ({ ...p, name: e.target.value }))}
              />
            </div>
            <div className="profile__form-row">
              <label>Роль</label>
              <div className="profile__roles">
                {[[false, '🎓 Студент'], [true, '👨‍🏫 Вчитель']].map(([val, lbl]) => (
                  <button
                    key={String(val)}
                    type="button"
                    className={`auth__role-btn ${profileForm.isTeacher === val ? 'auth__role-btn--active' : ''}`}
                    onClick={() => setProfileForm(p => ({ ...p, isTeacher: val }))}
                  >
                    {lbl}
                  </button>
                ))}
              </div>
            </div>
            <div className="profile__form-actions">
              <button
                className="btn btn--primary"
                type="button"
                onClick={saveProfile}
                disabled={savingProfile}
              >
                {savingProfile ? 'Збереження...' : 'Зберегти'}
              </button>
              {profileMessage && (
                <span className="profile__form-message">{profileMessage}</span>
              )}
            </div>
          </div>
        )}

        <div className="profile__stats">
          {[
            { icon: '👤', val: accaunt.login, lbl: 'Логін' },
            { icon: '🎓', val: accaunt.isTeacher ? 'Вчитель' : 'Студент', lbl: 'Роль' },
            { icon: '📝', val: loading ? '...' : myTests.length, lbl: 'Створено тестів' },
          ].map(s => (
            <div key={s.lbl} className="profile__stat">
              <span className="profile__stat-icon">{s.icon}</span>
              <span className="profile__stat-val">{s.val}</span>
              <span className="profile__stat-lbl">{s.lbl}</span>
            </div>
          ))}
        </div>

        {accaunt.isTeacher && (
          <div className="profile__section">
            <h2>Мої тести</h2>
            {loading ? (
              <p style={{ opacity: 0.5 }}>Завантаження...</p>
            ) : myTests.length === 0 ? (
              <p style={{ opacity: 0.5 }}>Ви ще не створили жодного тесту</p>
            ) : (
              <div className="profile__tests">
                {myTests.map(t => (
                  <div key={t.id} className="profile__test-item">
                    <span className="profile__test-name">{t.name}</span>
                    <span className="profile__test-meta">{t.questions?.length || 0} питань · {t.category}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}