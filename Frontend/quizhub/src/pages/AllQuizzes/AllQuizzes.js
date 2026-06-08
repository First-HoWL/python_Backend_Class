import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getApiJson } from '../../api';
import './AllQuizzes.scss';

const CATEGORIES = ['Всі', 'Програмування', 'Математика', 'Мови', 'Наука', 'Історія', 'Географія'];

export default function AllQuizzes() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('Всі');
  const [sort, setSort] = useState('newest');
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [rawData, setRawData] = useState(null);
  const [fetchError, setFetchError] = useState(null);

  useEffect(() => {
    setLoading(true);
    getApiJson('/api/tests')
      .then(data => {
        setRawData(data);
          const mapped = (data || []).map(t => ({
            id: t.id,
            title: t.name || t.title,
            category: 'Общее',
            tag: 'purple',
            questions: Array.isArray(t.questions) ? t.questions.length : 0,
            time: Array.isArray(t.questions) ? Math.max(1, t.questions.length) : 0,
            author: t.author?.name || t.author?.login || (typeof t.author === 'string' ? t.author : 'Автор'),
          }));
          setQuizzes(mapped);
        })
        .catch((err) => { console.error('Failed to load tests', err); setQuizzes([]); setFetchError(String(err)); })
      .finally(() => setLoading(false));
  }, []);

  const filtered = quizzes
    .filter(q => q.title.toLowerCase().includes(search.toLowerCase()))
    .filter(q => category === 'Всі' || q.category === category)
    .sort((a, b) => sort === 'questions' ? b.questions - a.questions : b.id - a.id);

  return (
    <div className="all-quizzes">
      <div className="container">
        <div className="page-header">
          <h1>Всі тести</h1>
          <p>Знайдіть тест за темою</p>
        </div>

        <div className="all-quizzes__toolbar">
          <div className="all-quizzes__search">
            <span>🔍</span>
            <input
              type="text"
              placeholder="Пошук за назвою або темою..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </div>
          <select value={sort} onChange={e => setSort(e.target.value)}>
              <option value="newest">Новіші</option>
              <option value="questions">За кількістю питань</option>
          </select>
        </div>

        <div className="all-quizzes__layout">
          <aside className="all-quizzes__sidebar">
            <div className="all-quizzes__filter-group">
              <h3>Кількість питань</h3>
              {['5–10', '10–20', '20+'].map(r => (
                <label key={r} className="all-quizzes__check">
                  <input type="checkbox" />
                  {r}
                </label>
              ))}
            </div>
          </aside>

          <div className="all-quizzes__main">
            <p className="all-quizzes__count">Знайдено: {filtered.length} тестів</p>
            {fetchError && <div style={{color:'red'}}>Помилка: {fetchError}</div>}
            {rawData && <details style={{marginTop:8}}><summary>Сирий відповідь /api/tests (debug)</summary><pre style={{maxHeight:300,overflow:'auto'}}>{JSON.stringify(rawData, null, 2)}</pre></details>}
            <div className="all-quizzes__grid">
              {loading ? (
                <p>Завантаження тестів...</p>
              ) : (
                filtered.map(q => (
                <Link to={`/quizzes/${q.id}`} key={q.id} className="card all-quizzes__card">
                  <span className={`tag tag--${q.tag}`}>{q.category}</span>
                  <h3>{q.title}</h3>
                  <div className="all-quizzes__card-meta">
                    <span>{q.questions} питань</span>
                    <span>{q.time} хв</span>
                  </div>
                  <div className="all-quizzes__card-foot">
                    <span className="all-quizzes__author">{q.author}</span>
                  </div>
                </Link>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
