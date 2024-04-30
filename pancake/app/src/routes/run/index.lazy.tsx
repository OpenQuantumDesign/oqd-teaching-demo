import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/run/")({
  component: () => <Run />,
});

import { ChangeEvent, useState } from "react";
import api from "../../lib/api";
import Loading from "../../components/Loading";

type gateModel = {
  gate: string;
  target: number;
  control?: number;
};

type circuitModel = {
  N: number;
  instructions: gateModel[];
};

type programModel = {
  clock: number;
  circuit: circuitModel;
};

const Run = () => {
  const [clock, setClock] = useState(1);

  const handleClockChange = (event: ChangeEvent<HTMLInputElement>) => {
    setClock(parseFloat(event.target.value));
  };

  ////////////////////////////////////////////////////////////////////////////////////////

  const [instructions, setInstructions] = useState<gateModel[]>([
    { gate: "I", target: 0 },
  ]);

  const handleInstructionsChange = (index: number) => {
    return (event: ChangeEvent<HTMLInputElement>) => {
      let new_instructions: Record<string, any>[] = [...instructions];
      new_instructions[index][event.target.name] =
        event.target.name === "gate"
          ? event.target.value
          : parseInt(event.target.value);

      setInstructions(new_instructions as gateModel[]);
    };
  };

  const handleAddSingleQubitGate = () => {
    setInstructions([...instructions, { gate: "I", target: 0 }]);
  };

  const handleAddTwoQubitGate = () => {
    setInstructions([...instructions, { gate: "CNOT", target: 1, control: 0 }]);
  };

  const handleRemoveGate = (index: number) => {
    if (instructions.length == 1) {
      return () => {};
    }
    return () => {
      setInstructions(instructions.filter((e, i) => i != index));
    };
  };

  ////////////////////////////////////////////////////////////////////////////////////////

  const [imageURL, setImageURL] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

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
        data: program,
      })
      .then((response) => response.data)
      .then((data) => URL.createObjectURL(data))
      .catch(() => {
        setImageURL("");
        setError(true);
      });

    const result = await api
      .request({
        method: "POST",
        url: "/api/run",
        headers: { "Content-Type": "application/json" },
        data: program,
      })
      .then((response) => response.data)
      .then((data) => JSON.stringify(JSON.parse(data), null, 2))
      .catch(() => {
        setImageURL("");
        setError(true);
      });

    if (url) {
      setImageURL(url);
    }

    if (result) {
      setResult(result);
    }

    setIsLoading(false);
  };

  ////////////////////////////////////////////////////////////////////////////////////////

  const program = {
    clock: clock,
    circuit: { N: 5, instructions: instructions },
  } as programModel;

  console.log(program);

  ////////////////////////////////////////////////////////////////////////////////////////

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
          <input
            className="w-16 rounded bg-base-300 p-2 text-sm outline outline-0"
            name="clock"
            placeholder="clock"
            value={clock}
            onChange={handleClockChange}
          />
          {instructions.map((element, index) => (
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
                    onChange={handleInstructionsChange(index)}
                  />
                </div>
              ))}
            </div>
          ))}
        </div>
        <div className="divider divider-vertical" />
        <div className="pl-5">
          <div className="card h-64 w-full cursor-text overflow-y-auto whitespace-pre bg-base-300 p-5 shadow-2xl">
            {JSON.stringify(program, null, 2)}
          </div>
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
          <div className="divider divider-vertical" />
          {result && (
            <div className="card h-64 w-full cursor-text overflow-y-auto whitespace-pre bg-base-300 p-5 shadow-2xl">
              {result}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
