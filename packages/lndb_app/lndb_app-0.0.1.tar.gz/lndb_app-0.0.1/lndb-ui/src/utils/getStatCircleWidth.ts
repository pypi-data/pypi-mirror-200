export const getStatCircleWidth = (count?: number) => {
  return count
    ? count < 99
      ? '1.5rem'
      : `${count.toString().length / 1.5}rem`
    : '1.5rem';
};
