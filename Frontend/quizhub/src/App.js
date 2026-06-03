import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';

import Home from './pages/Home/Home';
import AllQuizzes from './pages/AllQuizzes/AllQuizzes';
import QuizDetail from './pages/QuizDetail/QuizDetail';
import TakeQuiz from './pages/TakeQuiz/TakeQuiz';
import Results from './pages/Results/Results';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import TeacherDashboard from './pages/TeacherDashboard/TeacherDashboard';
import CreateQuiz from './pages/CreateQuiz/CreateQuiz';
import Profile from './pages/Profile/Profile';
import NotFound from './pages/NotFound/NotFound';

import './styles/global.scss';

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Navbar />
          <main style={{ flex: 1 }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/quizzes" element={<AllQuizzes />} />
              <Route path="/quizzes/:id" element={<QuizDetail />} />
              <Route path="/quizzes/:id/take" element={<TakeQuiz />} />
              <Route path="/quizzes/:id/results" element={<Results />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/teacher" element={<TeacherDashboard />} />
              <Route path="/teacher/create" element={<CreateQuiz />} />
              <Route path="/teacher/edit/:id" element={<CreateQuiz />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="*" element={<NotFound />} />
              <Route path="/404" element={<NotFound />} />
              <Route path="leaderboard" element={<TeacherDashboard />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </BrowserRouter>
    </ThemeProvider>
  );
}
