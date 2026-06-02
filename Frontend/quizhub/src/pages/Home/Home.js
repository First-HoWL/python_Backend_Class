import { Link } from 'react-router-dom';
import './Home.scss';

const FEATURED = [
  { id: 1, title: 'Основи Python', category: 'Програмування', tag: 'purple', questions: 20, time: 15, rating: 4.8 },
  { id: 2, title: 'Алгебра 9 клас', category: 'Математика', tag: 'teal', questions: 15, time: 20, rating: 4.5 },
  { id: 3, title: 'Англійська B1', category: 'Мови', tag: 'amber', questions: 30, time: 25, rating: 4.9 },
];

const FEATURES = [
  { icon: '🤖', title: 'AI-генерація питань', desc: 'Вкажи тему — отримай готові питання за секунди' },
  { icon: '📊', title: 'Детальна статистика', desc: 'Відстежуй прогрес і порівнюй результати з іншими' },
  { icon: '✏️', title: 'Кабінет вчителя', desc: 'Створюй, редагуй та керуй тестами легко' },
];

export default function Home() {
  return (
    <div className="home">
      <section className="home__hero">
        <div className="container">
          <div className="home__badge">AI-генерація питань</div>
          <h1 className="home__title">
            Платформа для<br />
            <span>розумних тестів</span>
          </h1>
          <p className="home__subtitle">
            Створюй тести за хвилини, проходь та порівнюй<br />
            результати з тисячами користувачів
          </p>
          <div className="home__btns">
            <Link to="/quizzes" className="btn btn--primary">Переглянути тести</Link>
            <Link to="/register" className="btn btn--outline">Створити тест</Link>
          </div>
        </div>
      </section>

      <section className="home__stats">
        <div className="container">
          {[['1 240', 'тестів'], ['8 500', 'користувачів'], ['42 000', 'проходжень']].map(([n, l]) => (
            <div key={l} className="home__stat">
              <span className="home__stat-num">{n}</span>
              <span className="home__stat-lbl">{l}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="home__featured">
        <div className="container">
          <div className="home__section-head">
            <h2>Популярні тести</h2>
            <Link to="/quizzes" className="home__see-all">Всі тести →</Link>
          </div>
          <div className="home__chips">
            {['Всі', 'Програмування', 'Математика', 'Мови', 'Наука'].map(c => (
              <span key={c} className={`home__chip ${c === 'Всі' ? 'home__chip--active' : ''}`}>{c}</span>
            ))}
          </div>
          <div className="home__cards">
            {FEATURED.map(q => (
              <Link to={`/quizzes/${q.id}`} key={q.id} className="card home__card">
                <span className={`tag tag--${q.tag}`}>{q.category}</span>
                <h3>{q.title}</h3>
                <div className="home__card-meta">
                  <span>{q.questions} питань</span>
                  <span>{q.time} хв</span>
                  <span className="home__card-rating">★ {q.rating}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="home__features">
        <div className="container">
          <h2 className="home__section-title">Чому QuizHub?</h2>
          <div className="home__features-grid">
            {FEATURES.map(f => (
              <div key={f.title} className="home__feature">
                <div className="home__feature-icon">{f.icon}</div>
                <h3>{f.title}</h3>
                <p>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="home__cta">
        <div className="container">
          <h2>Готовий почати?</h2>
          <p>Зареєструйся безкоштовно та створи свій перший тест</p>
          <Link to="/register" className="btn btn--primary">Зареєструватись</Link>
        </div>
      </section>
    </div>
  );
}
