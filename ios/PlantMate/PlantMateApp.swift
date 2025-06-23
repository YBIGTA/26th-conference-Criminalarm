import SwiftUI

@main
struct PlantMateApp: App {
    @State private var showIntro = true
    
    var body: some Scene {
        WindowGroup {
            if showIntro {
                IntroView(showIntro: $showIntro)
            } else {
                ContentView()
            }
        }
    }
} 