// Main JavaScript file for the Travel Booking application

document.addEventListener("DOMContentLoaded", () => {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))

  // Date picker initialization
  const datePickers = document.querySelectorAll(".datepicker")
  if (datePickers.length > 0) {
    datePickers.forEach((picker) => {
      picker.setAttribute("min", new Date().toISOString().split("T")[0])
    })
  }

  // Seat selection functionality
  const seatSelectors = document.querySelectorAll(".seat-selector")
  if (seatSelectors.length > 0) {
    seatSelectors.forEach((selector) => {
      selector.addEventListener("change", function () {
        const seats = Number.parseInt(this.value)
        const pricePerSeat = Number.parseFloat(this.dataset.price)
        const totalPriceElement = document.getElementById("total-price")

        if (totalPriceElement) {
          const totalPrice = seats * pricePerSeat
          totalPriceElement.textContent = totalPrice.toFixed(2)

          // Update hidden input for form submission
          const totalPriceInput = document.getElementById("id_total_price")
          if (totalPriceInput) {
            totalPriceInput.value = totalPrice.toFixed(2)
          }
        }
      })
    })
  }

  // Filter form functionality
  const filterForm = document.getElementById("filter-form")
  if (filterForm) {
    const clearButton = document.getElementById("clear-filters")
    if (clearButton) {
      clearButton.addEventListener("click", (e) => {
        e.preventDefault()
        const inputs = filterForm.querySelectorAll("input, select")
        inputs.forEach((input) => {
          if (input.type === "checkbox" || input.type === "radio") {
            input.checked = false
          } else {
            input.value = ""
          }
        })
        filterForm.submit()
      })
    }
  }
})

