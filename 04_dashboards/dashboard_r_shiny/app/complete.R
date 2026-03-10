install.packages("shiny")
install.packages("DT")

library(shiny)
library(dplyr)
library(ggplot2)
library(tidyr)
library(DT)
library(data.table)
library(scales)

setwd("/home/tatiane/repositorios/data-projects/04_dashboards/01_dashboard_r_shiny/raw/data/")
df <- fread("employee_attrition.csv", header = TRUE, dec = ".")

colnames(df)

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

server <- function(input, output) {
  
  filtered_data <- reactive({
    req(input$age, input$job, input$remote)
    
    df %>%
      filter(
        (input$job == "All" | .data$`Job Role` == input$job),
        (input$remote == "All" | .data$`Remote Work` == input$remote),
        Age >= input$age[1],
        Age <= input$age[2]
      )
  })
  
  output$kpi_total <- renderText({
    nrow(filtered_data())
  })
  
  output$kpi_attrition <- renderText({
    rate <- filtered_data() %>%
      summarise(rate = mean(Attrition == "Yes")) %>%
      pull(rate)
    
    percent(rate, accuracy = 0.1)
  })
  
  output$kpi_remote <- renderText({
    pct <- filtered_data() %>%
      summarise(pct = mean(`Remote Work` == "Yes")) %>%
      pull(pct)
    
    percent(pct, accuracy = 0.1)
  })
  
  output$attrition_plot <- renderPlot({
    filtered_data() %>%
      group_by(`Job Role`, Attrition) %>%
      summarise(n = n(), .groups = "drop") %>%
      ggplot(aes(x = `Job Role`, y = n, fill = Attrition)) +
      geom_col(position = "fill") +
      scale_y_continuous(labels = percent) +
      labs(
        title = "Attrition Rate by Job Role",
        x = "Job Role",
        y = "Proportion"
      ) +
      theme_minimal() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
  })
  
  output$remote_plot <- renderPlot({
    filtered_data() %>%
      group_by(`Remote Work`, Attrition) %>%
      summarise(n = n(), .groups = "drop") %>%
      ggplot(aes(x = `Remote Work`, y = n, fill = Attrition)) +
      geom_col(position = "fill") +
      scale_y_continuous(labels = percent) +
      labs(
        title = "Attrition by Remote Work",
        x = "Remote Work",
        y = "Proportion"
      ) +
      theme_minimal()
  })
  
  output$table <- renderDT({
    filtered_data()
  })
}

shinyApp(ui, server)
