document.addEventListener('DOMContentLoaded', () => {
  const dateInput = document.querySelector('input[name="booking_date"]');
  if (dateInput && !dateInput.value) {
    const d = new Date();
    d.setDate(d.getDate() + 1);
    dateInput.min = d.toISOString().split('T')[0];
  }
});
