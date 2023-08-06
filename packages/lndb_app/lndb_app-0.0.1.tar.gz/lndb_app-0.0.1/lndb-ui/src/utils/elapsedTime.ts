export const elapsedTime = (date: Date) => {
  const elapsedTimeMs = Date.now() - date.getTime();

  const elapsedTimeSeconds = Math.floor(elapsedTimeMs / 1000);
  if (elapsedTimeSeconds < 60) return `${elapsedTimeSeconds} seconds`;

  const elapsedTimeMinutes = Math.floor(elapsedTimeSeconds / 60);
  if (elapsedTimeMinutes == 1) return `${elapsedTimeMinutes} minute`;
  if (elapsedTimeMinutes < 60) return `${elapsedTimeMinutes} minutes`;

  const elapsedTimHours = Math.floor(elapsedTimeMinutes / 60);
  if (elapsedTimHours == 1) return `${elapsedTimHours} hour`;
  if (elapsedTimHours < 24) return `${elapsedTimHours} hours`;

  const elapsedTimeDays = Math.floor(elapsedTimHours / 24);
  if (elapsedTimeDays == 1) return `${elapsedTimeDays} day`;
  if (elapsedTimeDays < 7) return `${elapsedTimeDays} days`;

  const elapsedTimeWeeks = Math.floor(elapsedTimeDays / 7);
  if (elapsedTimeWeeks == 1) return `${elapsedTimeWeeks} week`;
  if (elapsedTimeWeeks < 5) return `${elapsedTimeWeeks} weeks`;

  const elapsedTimeMonths = Math.floor(elapsedTimeWeeks / 5);
  if (elapsedTimeMonths == 1) return `${elapsedTimeMonths} month`;
  return `${elapsedTimeMonths} months`;
};
