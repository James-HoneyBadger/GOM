use eframe::egui;
use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;
use std::sync::mpsc;
use syntect::easy::HighlightLines;
use syntect::highlighting::{ThemeSet, Style};
use syntect::parsing::SyntaxSet;
use syntect::util::{as_24_bit_terminal_escaped, LinesWithEndings};

// Import our interpreter modules
mod base;
mod builtin;
mod interpreter;
mod processor;
mod serialize;

use crate::interpreter::Interpreter;
use crate::processor::syntax_tree::generate_syntax_tree;
use crate::processor::lexer::tokenize;

#[derive(Default)]
struct DreamberdIDE {
    code: String,
    output: String,
    current_file: Option<PathBuf>,
    breakpoints: HashMap<usize, bool>,
    variables: HashMap<String, String>,
    is_running: bool,
    debug_mode: bool,
    current_line: usize,
    font_size: f32,
    theme: Theme,
    show_debug_panel: bool,
    // Syntax highlighting
    syntax_set: SyntaxSet,
    theme_set: ThemeSet,
    highlighted_code: Vec<(syntect::highlighting::Style, String)>,
}

#[derive(Debug, Clone, Copy, PartialEq)]
enum Theme {
    Light,
    Dark,
    Custom,
}

impl Default for Theme {
    fn default() -> Self {
        Theme::Dark
    }
}

impl DreamberdIDE {
    fn new(_cc: &eframe::CreationContext<'_>) -> Self {
        let syntax_set = SyntaxSet::load_defaults_newlines();
        let theme_set = ThemeSet::load_defaults();

        let mut ide = Self {
            code: "print 'Hello, DreamBerd!'!".to_string(),
            output: "Welcome to DreamBerd IDE!\n".to_string(),
            font_size: 12.0,
            show_debug_panel: false,
            syntax_set,
            theme_set,
            highlighted_code: Vec::new(),
            ..Default::default()
        };

        ide.update_syntax_highlighting();
        ide
    }

    fn run_code(&mut self) {
        self.output.push_str("Running DreamBerd code...\n");
        self.is_running = true;

        // Tokenize
        let tokens = match tokenize("ide_input", &self.code) {
            Ok(t) => t,
            Err(e) => {
                self.output.push_str(&format!("Tokenization error: {}\n", e));
                self.is_running = false;
                return;
            }
        };

        // Parse
        let syntax_tree = match generate_syntax_tree("ide_input", tokens, &self.code) {
            Ok(st) => st,
            Err(e) => {
                self.output.push_str(&format!("Parse error: {}\n", e));
                self.is_running = false;
                return;
            }
        };

        // Execute
        let mut interpreter = Interpreter::new("ide_input".to_string(), self.code.clone());
        if let Err(e) = interpreter.interpret_code_statements(syntax_tree) {
            self.output.push_str(&format!("Execution error: {}\n", e));
        } else {
            self.output.push_str("Execution completed successfully!\n");
        }

        self.is_running = false;
        self.update_syntax_highlighting();
    }

    fn clear_output(&mut self) {
        self.output.clear();
    }

    fn new_file(&mut self) {
        self.code = String::new();
        self.current_file = None;
        self.output = "New file created\n".to_string();
        self.update_syntax_highlighting();
    }

    fn update_syntax_highlighting(&mut self) {
        let syntax = self.syntax_set.find_syntax_by_extension("rs").unwrap_or_else(|| {
            self.syntax_set.find_syntax_plain_text()
        });

        let theme = match self.theme {
            Theme::Light => &self.theme_set.themes["InspiredGitHub"],
            Theme::Dark => &self.theme_set.themes["base16-mocha.dark"],
            Theme::Custom => &self.theme_set.themes["base16-ocean.dark"],
        };

        let mut highlighter = HighlightLines::new(syntax, theme);
        self.highlighted_code.clear();

        for line in LinesWithEndings::from(&self.code) {
            let ranges = highlighter.highlight_line(line, &self.syntax_set).unwrap_or_default();
            for (style, text) in ranges {
                self.highlighted_code.push((style, text.to_string()));
            }
        }
    }

    fn open_file(&mut self) {
        if let Some(path) = rfd::FileDialog::new()
            .add_filter("DreamBerd files", &["db"])
            .add_filter("All files", &["*"])
            .pick_file()
        {
            match fs::read_to_string(&path) {
                Ok(content) => {
                    self.code = content;
                    self.current_file = Some(path.clone());
                    self.output = format!("Opened file: {}\n", path.display());
                    self.update_syntax_highlighting();
                }
                Err(e) => {
                    self.output = format!("Error opening file: {}\n", e);
                }
            }
        }
    }

    fn save_file(&mut self) {
        if let Some(path) = &self.current_file {
            match fs::write(path, &self.code) {
                Ok(_) => self.output = format!("Saved to {}\n", path.display()),
                Err(e) => self.output = format!("Save error: {}\n", e),
            }
        } else {
            self.save_file_as();
        }
    }

    fn save_file_as(&mut self) {
        if let Some(path) = rfd::FileDialog::new()
            .add_filter("DreamBerd files", &["db"])
            .add_filter("All files", &["*"])
            .save_file()
        {
            match fs::write(&path, &self.code) {
                Ok(_) => {
                    self.current_file = Some(path.clone());
                    self.output = format!("Saved to {}\n", path.display());
                }
                Err(e) => self.output = format!("Save error: {}\n", e),
            }
        }
    }

    fn toggle_breakpoint(&mut self, line: usize) {
        let enabled = self.breakpoints.get(&line).unwrap_or(&false);
        self.breakpoints.insert(line, !enabled);
    }

    fn get_theme_colors(&self) -> (egui::Color32, egui::Color32, egui::Color32) {
        match self.theme {
            Theme::Light => (egui::Color32::WHITE, egui::Color32::BLACK, egui::Color32::LIGHT_GRAY),
            Theme::Dark => (egui::Color32::from_rgb(30, 30, 30), egui::Color32::WHITE, egui::Color32::from_rgb(60, 60, 60)),
            Theme::Custom => (egui::Color32::from_rgb(20, 20, 40), egui::Color32::from_rgb(200, 200, 255), egui::Color32::from_rgb(40, 40, 80)),
        }
    }
}

impl eframe::App for DreamberdIDE {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        let (bg_color, text_color, panel_color) = self.get_theme_colors();

        egui::CentralPanel::default()
            .frame(egui::Frame::none().fill(bg_color))
            .show(ctx, |ui| {
                ui.style_mut().visuals.override_text_color = Some(text_color);

                // Menu bar
                ui.horizontal(|ui| {
                    ui.heading("DreamBerd IDE");

                    ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                        // Theme selector
                        ui.horizontal(|ui| {
                            ui.label("Theme:");
                            if ui.selectable_label(matches!(self.theme, Theme::Light), "Light").clicked() {
                                self.theme = Theme::Light;
                                self.update_syntax_highlighting();
                            }
                            if ui.selectable_label(matches!(self.theme, Theme::Dark), "Dark").clicked() {
                                self.theme = Theme::Dark;
                                self.update_syntax_highlighting();
                            }
                            if ui.selectable_label(matches!(self.theme, Theme::Custom), "Custom").clicked() {
                                self.theme = Theme::Custom;
                                self.update_syntax_highlighting();
                            }
                        });

                        ui.checkbox(&mut self.show_debug_panel, "Debug Panel");
                        ui.checkbox(&mut self.debug_mode, "Debug Mode");

                        if ui.button("New").clicked() {
                            self.new_file();
                        }
                        if ui.button("Open").clicked() {
                            self.open_file();
                        }
                        if ui.button("Save").clicked() {
                            self.save_file();
                        }
                        if ui.button("Run").clicked() {
                            self.run_code();
                        }
                        if ui.button("Clear").clicked() {
                            self.clear_output();
                        }
                    });
                });

                ui.separator();

                // Main content area
                if self.show_debug_panel {
                    ui.columns(3, |columns| {
                        // Code Editor Panel
                        columns[0].vertical(|ui| {
                            ui.label("Code Editor");
                            egui::ScrollArea::vertical().show(ui, |ui| {
                                let mut code_changed = false;
                                let response = ui.add(
                                    egui::TextEdit::multiline(&mut self.code)
                                        .font(egui::FontId::monospace(self.font_size))
                                        .desired_width(f32::INFINITY)
                                        .desired_rows(25)
                                );
                                if response.changed() {
                                    code_changed = true;
                                }

                                // Update syntax highlighting if code changed
                                if code_changed {
                                    self.update_syntax_highlighting();
                                }
                            });
                        });

                        // Output Panel
                        columns[1].vertical(|ui| {
                            ui.label("Output");
                            egui::ScrollArea::vertical().show(ui, |ui| {
                                ui.add(
                                    egui::TextEdit::multiline(&mut self.output)
                                        .font(egui::FontId::monospace(self.font_size))
                                        .desired_width(f32::INFINITY)
                                        .desired_rows(25)
                                );
                            });
                        });

                        // Debug Panel
                        columns[2].vertical(|ui| {
                            ui.label("Debug Panel");
                            egui::ScrollArea::vertical().show(ui, |ui| {
                                ui.group(|ui| {
                                    ui.label("Variables:");
                                    for (name, value) in &self.variables {
                                        ui.label(format!("{} = {}", name, value));
                                    }
                                });

                                ui.separator();

                                ui.group(|ui| {
                                    ui.label("Breakpoints:");
                                    for (line, enabled) in &self.breakpoints {
                                        if *enabled {
                                            ui.label(format!("Line {}", line));
                                        }
                                    }
                                });
                            });
                        });
                    });
                } else {
                    ui.columns(2, |columns| {
                        // Code Editor Panel
                        columns[0].vertical(|ui| {
                            ui.label("Code Editor");
                            egui::ScrollArea::vertical().show(ui, |ui| {
                                let mut code_changed = false;
                                let response = ui.add(
                                    egui::TextEdit::multiline(&mut self.code)
                                        .font(egui::FontId::monospace(self.font_size))
                                        .desired_width(f32::INFINITY)
                                        .desired_rows(25)
                                );
                                if response.changed() {
                                    code_changed = true;
                                }

                                // Update syntax highlighting if code changed
                                if code_changed {
                                    self.update_syntax_highlighting();
                                }
                            });
                        });

                        // Output Panel
                        columns[1].vertical(|ui| {
                            ui.label("Output");
                            egui::ScrollArea::vertical().show(ui, |ui| {
                                ui.add(
                                    egui::TextEdit::multiline(&mut self.output)
                                        .font(egui::FontId::monospace(self.font_size))
                                        .desired_width(f32::INFINITY)
                                        .desired_rows(25)
                                );
                            });
                        });
                    });
                }

                // Status bar
                ui.separator();
                ui.horizontal(|ui| {
                    if let Some(file) = &self.current_file {
                        ui.label(format!("File: {}", file.display()));
                    } else {
                        ui.label("No file open");
                    }

                    ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                        ui.label(format!("Font Size: {:.0}", self.font_size));
                        if ui.button("-").clicked() && self.font_size > 8.0 {
                            self.font_size -= 1.0;
                        }
                        if ui.button("+").clicked() && self.font_size < 24.0 {
                            self.font_size += 1.0;
                        }

                        ui.label(format!("Line: {}", self.current_line));
                        if self.is_running {
                            ui.label("Running...");
                        } else {
                            ui.label("Ready");
                        }
                    });
                });
            });
    }
}

fn main() -> eframe::Result<()> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([1400.0, 900.0])
            .with_title("DreamBerd IDE"),
        ..Default::default()
    };

    eframe::run_native(
        "DreamBerd IDE",
        options,
        Box::new(|cc| Box::new(DreamberdIDE::new(cc))),
    )
}