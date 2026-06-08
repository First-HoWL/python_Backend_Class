import { Link, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getApiJson } from '../../api';
import './QuizDetail.scss';

const REVIEWS = [
  { name: 'Катерина М.', score: 18, total: 20, comment: 'Дуже корисний тест, допоміг закріпити знання!' },
  { name: 'Артем В.', score: 15, total: 20, comment: 'Деякі питання були непростими, але загалом добре.' },
];

export default function QuizDetail() {
  const { id } = useParams();
  const [quiz, setQuiz] = useState(null);

  useEffect(() => {
    getApiJson('/api/tests')
      .then(data => {
        const t = data.find(x => String(x.id) === String(id));
        if (t) {
          setQuiz({
            id: t.id,
            title: t.name || t.title,
            description: t.description || '',
            category: 'Общее',
            tag: 'purple',
            questions: Array.isArray(t.questions) ? t.questions.length : 0,
            time: Array.isArray(t.questions) ? Math.max(1, t.questions.length) : 0,
            author: t.author?.name || t.author?.login || (typeof t.author === 'string' ? t.author : 'Автор'),
            createdAt: t.createdAt || ''
          });
        } else {
          setQuiz(null);
        }
      })
      .catch((err) => { console.error('Failed to load tests for detail', err); setQuiz(null); });
  }, [id]);

  if (!quiz) return <div className="container">Тест не знайдено або завантажується...</div>;

  return (
    <div className="quiz-detail">
      <div className="container">
        <div className="quiz-detail__layout">

          <div className="quiz-detail__main">
            <span className={`tag tag--${quiz.tag}`}>{quiz.category}</span>
            <h1 className="quiz-detail__title">{quiz.title}</h1>
            <p className="quiz-detail__desc">{quiz.description}</p>

            <div className="quiz-detail__meta-row">
              <div className="quiz-detail__meta-item">
                <span className="quiz-detail__meta-icon">📋</span>
                <div>
                  <span className="quiz-detail__meta-label">Питань</span>
                  <span className="quiz-detail__meta-val">{quiz.questions}</span>
                </div>
              </div>
              <div className="quiz-detail__meta-item">
                <span className="quiz-detail__meta-icon">⏱</span>
                <div>
                  <span className="quiz-detail__meta-label">Час</span>
                  <span className="quiz-detail__meta-val">{quiz.time} хв</span>
                </div>
              </div>
            </div>

            <div className="quiz-detail__reviews">
              <h2>Відгуки</h2>
              {REVIEWS.map((r, i) => (
                <div key={i} className="quiz-detail__review">
                  <div className="quiz-detail__review-head">
                    <span className="quiz-detail__review-name">{r.name}</span>
                    <span className="quiz-detail__review-score">{r.score}/{r.total}</span>
                  </div>
                  <p>{r.comment}</p>
                </div>
              ))}
            </div>
          </div>

          <aside className="quiz-detail__sidebar">
            <div className="quiz-detail__start-card">
              <Link to={`/quizzes/${id}/take`} className="btn btn--primary quiz-detail__start-btn">
                Почати тест
              </Link>
              <div className="quiz-detail__author">
                <div className="quiz-detail__avatar">ОП</div>
                <div>
                  <span className="quiz-detail__author-label">Автор</span>
                  <span className="quiz-detail__author-name">{quiz.author}</span>
                </div>
              </div>
              <span className="quiz-detail__date">Створено {quiz.createdAt}</span>
            </div>
          </aside>

        </div>
      </div>
    </div>
  );
}
