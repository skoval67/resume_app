import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getResume, improveResume } from "../api";

export default function ResumeDetail() {
  const { id } = useParams();
  const [resume, setResume] = useState(null);

  const fetchData = async () => {
    setResume(await getResume(id));
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  const handleImprove = async () => {
    await improveResume(id);
    await fetchData();
  };

  if (!resume) return <p>Загрузка...</p>;

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl mb-2">{resume.title}</h1>
      <pre className="border p-4 rounded whitespace-pre-wrap">{resume.content}</pre>
      <button className="mt-4 bg-purple-600 text-white p-2 rounded" onClick={handleImprove}>
        Улучшить
      </button>
    </div>
  );
}
