export const randomN = (props: { mu: number; sigma: number }) => {
  const z =
    Math.sqrt(-2 * Math.log(Math.random())) *
    Math.cos(2 * Math.PI * Math.random());

  return props.mu + props.sigma * z;
};
