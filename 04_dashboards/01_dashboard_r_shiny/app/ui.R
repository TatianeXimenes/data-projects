library(shiny)
library(DT)

ui <- fluidPage(
  titlePanel("Employee Attrition Dashboard"),
  
  fluidRow(
    column(4, wellPanel(
      h4("Attrition Rate"),
      textOutput("kpi_attrition")
    )),
    column(4, wellPanel(
      h4("Total Employees"),
      textOutput("kpi_total")
    )),
    column(4, wellPanel(
      h4("Remote Workers (%)"),
      textOutput("kpi_remote")
    ))
  ),
  
  sidebarLayout(
    sidebarPanel(
      selectInput(
        "job",
        "Job Role:",
        choices = c("All", sort(unique(df$`Job Role`))),
        selected = "All"
      ),
      
      selectInput(
        "remote",
        "Remote Work:",
        choices = c("All", "Yes", "No"),
        selected = "All"
      ),
      
      sliderInput(
        "age",
        "Age Range:",
        min = min(df$Age, na.rm = TRUE),
        max = max(df$Age, na.rm = TRUE),
        value = c(min(df$Age), max(df$Age))
      )
    ),
    
    mainPanel(
      plotOutput("attrition_plot"),
      plotOutput("remote_plot"),
      DTOutput("table")
    )
  )
)