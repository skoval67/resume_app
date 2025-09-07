import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getResumes, createResume } from "../api";

export default function Resumes() {
  const [resumes, setResumes] = useState([]);
  const [title, setTitle] = useState("");

  const fetchData = async () => {
    setResumes(await getResumes());
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreate = async () => {
    if (!title) return;
    await createResume({ title, content: "" });
    setTitle("");
    fetchData();
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl mb-4">Мои резюме</h1>
      <div className="flex gap-2 mb-4">
        <input
          className="border p-2 flex-1 rounded"
          placeholder="Название резюме"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button className="bg-green-600 text-white p-2 rounded" onClick={handleCreate}>
          Добавить
        </button>
      </div>
      <ul className="space-y-2">
        {resumes.map(r => (
          <li key={r.id} className="border p-2 rounded">
            <Link to={`/resumes/${r.id}`} className="text-blue-600 underline">
              {r.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
