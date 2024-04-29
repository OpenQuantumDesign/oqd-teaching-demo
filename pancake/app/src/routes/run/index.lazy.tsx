import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/run/")({
  component: () => <Run />,
});

import { ChangeEvent, useState } from "react";
import api from "../../lib/api";
import Loading from "../../components/Loading";

type gate = {
  gate: string;
  target: number;
  control?: number;
};

type circuit = {
  N: number;
  instructions: gate[];
};

const Run = () => {
  const [form, setForm] = useState<circuit>({
    N: 5,
    instructions: [{ gate: "I", target: 0 }],
  });

  const [imageURL, setImageURL] = useState("");
  const [error, setError] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (index: number) => {
    return (event: ChangeEvent<HTMLInputElement>) => {
      let new_instructions: Record<string, any>[] = [...form.instructions];
      new_instructions[index][event.target.name] = event.target.value;

      setForm((prev) => {
        return { N: prev.N, instructions: new_instructions as gate[] };
      });
    };
  };

  const handleAddSingleQubitGate = () => {
    let new_instructions: gate[] = [...form.instructions];
    new_instructions.push({ gate: "I", target: 0 });
    setForm((prev) => {
      return { N: prev.N, instructions: new_instructions };
    });
  };

  const handleAddTwoQubitGate = () => {
    let new_instructions: gate[] = [...form.instructions];
    new_instructions.push({ gate: "CNOT", target: 0, control: 1 });
    setForm((prev) => {
      return { N: prev.N, instructions: new_instructions };
    });
  };

  const handleRemoveGate = (index: number) => {
    if (form.instructions.length == 1) {
      return () => {};
    }
    return () => {
      setForm((prev) => {
        return {
          N: prev.N,
          instructions: prev.instructions.filter((e, i) => i != index),
        };
      });
    };
  };

  const handleSubmit = async () => {
    setImageURL("");
    setIsLoading(true);
    setError(false);

    const url = await api
      .request({
        method: "POST",
        url: "/api/visualize",
        responseType: "blob",
        headers: { "Content-Type": "application/json" },
        data: form,
      })
      .then((response) => response.data)
      .then((data) => URL.createObjectURL(data))
      .catch(() => {
        setImageURL("");
        setError(true);
      });

    if (url) {
      setImageURL(url);
    }
    setIsLoading(false);
  };

  return (
    <div className="flex flex-row flex-wrap gap-8">
      <div className="w-[32rem] ">
        <div className="flex flex-row place-content-center gap-3 py-5">
          <button
            className="btn btn-primary btn-sm"
            onClick={handleAddSingleQubitGate}
          >
            Single Qubit Gate
          </button>
          <button
            className="btn btn-primary btn-sm"
            onClick={handleAddTwoQubitGate}
          >
            Two Qubit Gate
          </button>
        </div>
        <div className="flex h-64 w-full flex-col gap-y-3 overflow-y-auto px-5">
          {form.instructions.map((element, index) => (
            <div
              key={"gate" + index}
              className="flex flex-row items-center gap-3"
            >
              <button
                className="btn btn-circle btn-sm"
                onClick={handleRemoveGate(index)}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="h-6 w-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M6 18 18 6M6 6l12 12"
                  />
                </svg>
              </button>
              {Object.entries(element).map((element2) => (
                <div key={"gate" + index + element2[0]}>
                  <input
                    className="w-16 rounded bg-base-300 p-2 text-sm outline outline-0"
                    name={element2[0]}
                    placeholder={element2[0]}
                    value={element2[1]}
                    onChange={handleChange(index)}
                  />
                </div>
              ))}
            </div>
          ))}
        </div>
        <div className="divider divider-vertical" />
        <div className="pl-5">
          <p className="h-64 w-full cursor-text overflow-y-auto whitespace-pre bg-base-300 p-5">
            {JSON.stringify(form, null, 2)}
          </p>
        </div>
      </div>
      <div className="divider divider-horizontal">
        <button
          className={
            isLoading ? "btn btn-disabled btn-primary" : "btn btn-primary"
          }
          onClick={handleSubmit}
        >
          {isLoading ? (
            <span className="loading loading-spinner"></span>
          ) : (
            "Submit"
          )}
        </button>
      </div>
      <div className="flex flex-col place-content-center">
        <div className="py-5">
          {imageURL && (
            <div className="card w-[48rem] bg-base-300 p-5 shadow-2xl">
              <img src={imageURL}></img>
            </div>
          )}
          {isLoading && (
            <div className="card w-[48rem] bg-base-300 p-5 shadow-2xl">
              <Loading />
            </div>
          )}
          {error && (
            <div className="alert alert-error w-[48rem]">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="h-6 w-6"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
                />
              </svg>
              Error
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
