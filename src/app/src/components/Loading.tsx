import {
  useTrail,
  useChain,
  useSprings,
  animated,
  useSpringRef,
} from "@react-spring/web";

////////////////////////////////////////////////////////////////////////////////////////

import { randomN } from "../lib/random";

////////////////////////////////////////////////////////////////////////////////////////

export default function Loading() {
  const STROKE_WIDTH = 0.1;

  const OFFSET = STROKE_WIDTH / 2;

  const MAX_WIDTH = 200 + OFFSET * 2;
  const MAX_HEIGHT = 50 + OFFSET * 2;

  const COORDS = [...Array(160)].map((e2, i2) =>
    [...Array(2)].map(
      (e, i) =>
        (~~(randomN({ mu: 0.5, sigma: 0.1 }) * 5) + -(i - 1) * (i2 % 4) * 5) *
        10,
    ),
  );

  const gridApi = useSpringRef();
  const gridSprings = useTrail(21, {
    ref: gridApi,
    from: {
      x2: 0,
      y2: 0,
    },
    to: {
      x2: MAX_WIDTH,
      y2: MAX_HEIGHT,
    },
    config: { duration: 50 },
  });

  // const boxApi = useSpringRef();

  const [boxSprings] = useSprings(160, (i) => ({
    from: { opacity: 0 },
    to: async (next) => {
      await next({ opacity: 1 });
      await next({ opacity: 0 });
    },
    loop: true,
    delay: i * 200,
    config: {
      duration: 1000,
    },
  }));

  useChain([gridApi], [0, 1], 1000);

  return (
    <svg viewBox={`0 0 ${MAX_WIDTH} ${MAX_HEIGHT}`}>
      <g>
        {gridSprings.map(({ x2 }, index) => (
          <animated.line
            x1={0}
            y1={index * 10 + OFFSET}
            x2={x2}
            y2={index * 10 + OFFSET}
            key={index}
            strokeWidth={STROKE_WIDTH}
            stroke="currentColor"
          />
        ))}
        {gridSprings.map(({ y2 }, index) => (
          <animated.line
            x1={index * 10 + OFFSET}
            y1={0}
            x2={index * 10 + OFFSET}
            y2={y2}
            key={index}
            strokeWidth={STROKE_WIDTH}
            stroke="currentColor"
          />
        ))}
      </g>
      {boxSprings.map(({ opacity }, index) => (
        <animated.rect
          key={index}
          width={10}
          height={10}
          fill="currentColor"
          style={{
            transformOrigin: `${5 + OFFSET * 2}px ${5 + OFFSET * 2}px`,
            transform: `translate(${COORDS[index][0] + OFFSET}px, ${COORDS[index][1] + OFFSET}px)`,
            opacity,
          }}
        />
      ))}
    </svg>
  );
}
