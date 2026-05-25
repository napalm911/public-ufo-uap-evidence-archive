import { Routes, Route } from "react-router-dom";
import AppShell from "./layout/AppShell";
import HomePage from "./pages/HomePage";
import SourcePage from "./pages/SourcePage";
import DocumentPage from "./pages/DocumentPage";
import TimelinePage from "./pages/TimelinePage";
import TopicsPage from "./pages/TopicsPage";
import TopicPage from "./pages/TopicPage";
import AskPage from "./pages/AskPage";
import SearchPage from "./pages/SearchPage";
import "./pages/pages.css";

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/sources/:sourceKey" element={<SourcePage />} />
        <Route path="/documents/:docId" element={<DocumentPage />} />
        <Route path="/timeline" element={<TimelinePage />} />
        <Route path="/topics" element={<TopicsPage />} />
        <Route path="/topics/:topicKey" element={<TopicPage />} />
        <Route path="/ask" element={<AskPage />} />
        <Route path="/search" element={<SearchPage />} />
      </Routes>
    </AppShell>
  );
}
