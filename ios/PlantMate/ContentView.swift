import SwiftUI

struct ContentView: View {
    @State private var animateCharacter = false
    @State private var selectedDate = 21
    @State private var showChatView = false
    @State private var showMenu = false
    @State private var showReportView = false
    @State private var showCheckupView = false
    
    let dates = [16, 17, 18, 19, 20, 21, 22]
    
    var body: some View {
        NavigationView {
            GeometryReader { geometry in
                ZStack {
                    // Background
                    Color(red: 234/255, green: 230/255, blue: 213/255)
                        .ignoresSafeArea()
                    
                    VStack(spacing: 0) {
                        // Status Bar 영역
                        Rectangle()
                            .fill(Color.clear)
                            .frame(height: 62)
                        
                        // Header
                        HStack {
                            Text("PlantMate")
                                .font(.system(size: 32, weight: .regular, design: .rounded))
                                .foregroundColor(Color(red: 3/255, green: 158/255, blue: 8/255))
                            
                            Spacer()
                            
                            Button(action: {
                                showMenu = true
                            }) {
                                Image(systemName: "line.3.horizontal")
                                    .font(.system(size: 24))
                                    .foregroundColor(.black)
                            }
                        }
                        .padding(.horizontal, 20)
                        .padding(.bottom, 20)
                        
                        ScrollView {
                            VStack(spacing: 16) {
                                // Date and Refresh
                                HStack {
                                    Text("6월 21일 토요일")
                                        .font(.system(size: 20, weight: .medium))
                                        .foregroundColor(.black)
                                    
                                    Button(action: {}) {
                                        Image(systemName: "arrow.clockwise")
                                            .font(.system(size: 16))
                                            .foregroundColor(.black)
                                    }
                                }
                                .padding(.horizontal, 20)
                                
                                // Main Card
                                VStack(spacing: 20) {
                                    // Status Card
                                    VStack(spacing: 16) {
                                        // Status Header
                                        HStack {
                                            Rectangle()
                                                .fill(Color(red: 3/255, green: 158/255, blue: 8/255))
                                                .frame(height: 20)
                                                .cornerRadius(10)
                                        }
                                        
                                        // Status Values
                                        HStack(spacing: 0) {
                                            // Temperature
                                            VStack(spacing: 8) {
                                                Text("온도")
                                                    .font(.system(size: 13, weight: .medium))
                                                    .foregroundColor(.white)
                                                    .padding(.horizontal, 12)
                                                    .padding(.vertical, 4)
                                                    .background(Color(red: 3/255, green: 158/255, blue: 8/255))
                                                    .cornerRadius(8)
                                                
                                                HStack(alignment: .bottom, spacing: 2) {
                                                    Text("21")
                                                        .font(.system(size: 32, weight: .medium))
                                                    Text("°C")
                                                        .font(.system(size: 20, weight: .medium))
                                                }
                                                .foregroundColor(.black)
                                                
                                                Text("딱 좋아요")
                                                    .font(.system(size: 14))
                                                    .foregroundColor(.black)
                                            }
                                            .frame(maxWidth: .infinity)
                                            
                                            // Humidity
                                            VStack(spacing: 8) {
                                                Text("습도")
                                                    .font(.system(size: 13, weight: .medium))
                                                    .foregroundColor(.white)
                                                    .padding(.horizontal, 12)
                                                    .padding(.vertical, 4)
                                                    .background(Color(red: 3/255, green: 158/255, blue: 8/255))
                                                    .cornerRadius(8)
                                                
                                                HStack(alignment: .bottom, spacing: 2) {
                                                    Text("80")
                                                        .font(.system(size: 32, weight: .medium))
                                                    Text("%")
                                                        .font(.system(size: 20, weight: .medium))
                                                }
                                                .foregroundColor(.black)
                                                
                                                Text("축축해요...")
                                                    .font(.system(size: 14))
                                                    .foregroundColor(.black)
                                            }
                                            .frame(maxWidth: .infinity)
                                            
                                            // Light
                                            VStack(spacing: 8) {
                                                Text("조도")
                                                    .font(.system(size: 13, weight: .medium))
                                                    .foregroundColor(.white)
                                                    .padding(.horizontal, 12)
                                                    .padding(.vertical, 4)
                                                    .background(Color(red: 3/255, green: 158/255, blue: 8/255))
                                                    .cornerRadius(8)
                                                
                                                HStack(alignment: .bottom, spacing: 2) {
                                                    Text("10")
                                                        .font(.system(size: 32, weight: .medium))
                                                    Text("%")
                                                        .font(.system(size: 20, weight: .medium))
                                                }
                                                .foregroundColor(.black)
                                                
                                                Text("잠이 온다...")
                                                    .font(.system(size: 14))
                                                    .foregroundColor(.black)
                                            }
                                            .frame(maxWidth: .infinity)
                                        }
                                    }
                                    .padding(.horizontal, 20)
                                    .padding(.vertical, 16)
                                    .background(Color.white)
                                    .cornerRadius(15)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 15)
                                            .stroke(Color(red: 3/255, green: 158/255, blue: 8/255), lineWidth: 2)
                                    )
                                    
                                    // Plant Info
                                    VStack(spacing: 12) {
                                        Text("스킨답서스")
                                            .font(.system(size: 10))
                                            .foregroundColor(.black)
                                        
                                        Text("그루트")
                                            .font(.system(size: 20, weight: .medium))
                                            .foregroundColor(.black)
                                        
                                        HStack {
                                            Text("\"신조오 사사게요!\"")
                                                .font(.system(size: 20, weight: .medium))
                                                .foregroundColor(.black)
                                            
                                            // Chat Button - 채팅 화면으로 이동
                                            Button(action: {
                                                showChatView = true
                                            }) {
                                                Image(systemName: "bubble.left.fill")
                                                    .font(.system(size: 16))
                                                    .foregroundColor(.gray)
                                            }
                                        }
                                        
                                        // Plant Character
                                        PlantMainCharacterView()
                                            .scaleEffect(animateCharacter ? 1.0 : 0.8)
                                            .animation(.spring(response: 0.8, dampingFraction: 0.6), value: animateCharacter)
                                    }
                                }
                                .padding(.horizontal, 20)
                                .padding(.vertical, 20)
                                .background(Color.white)
                                .cornerRadius(20)
                                .padding(.horizontal, 20)
                                
                                // Calendar
                                CalendarView(selectedDate: $selectedDate, dates: dates)
                                    .padding(.horizontal, 20)
                                
                                // Action Buttons
                                HStack(spacing: 16) {
                                    // Report Button
                                    Button(action: {
                                        showReportView = true
                                    }) {
                                        VStack(spacing: 8) {
                                            HStack {
                                                Text("Report")
                                                    .font(.system(size: 24, weight: .medium, design: .rounded))
                                                    .foregroundColor(.white)
                                                
                                                Spacer()
                                                
                                                Image(systemName: "chevron.right")
                                                    .font(.system(size: 14, weight: .medium))
                                                    .foregroundColor(.white)
                                            }
                                            
                                            Spacer()
                                            
                                            Text("주간 리포트")
                                                .font(.system(size: 20, weight: .medium))
                                                .foregroundColor(.white)
                                        }
                                        .padding(16)
                                        .frame(height: 146)
                                        .frame(maxWidth: .infinity)
                                        .background(Color(red: 157/255, green: 175/255, blue: 131/255))
                                        .cornerRadius(15)
                                    }
                                    
                                    // Checkup Button
                                    Button(action: {
                                        showCheckupView = true
                                    }) {
                                        VStack(spacing: 8) {
                                            HStack {
                                                Text("Checkup")
                                                    .font(.system(size: 24, weight: .medium, design: .rounded))
                                                    .foregroundColor(.white)
                                                
                                                Spacer()
                                                
                                                Image(systemName: "chevron.right")
                                                    .font(.system(size: 14, weight: .medium))
                                                    .foregroundColor(.white)
                                            }
                                            
                                            Spacer()
                                            
                                            Text("상태 확인하기")
                                                .font(.system(size: 20, weight: .medium))
                                                .foregroundColor(.white)
                                        }
                                        .padding(16)
                                        .frame(height: 146)
                                        .frame(maxWidth: .infinity)
                                        .background(Color(red: 157/255, green: 175/255, blue: 131/255))
                                        .cornerRadius(15)
                                    }
                                }
                                .padding(.horizontal, 20)
                                .padding(.bottom, 40)
                            }
                        }
                        
                        // Home Indicator 영역
                        Rectangle()
                            .fill(Color.clear)
                            .frame(height: 34)
                    }
                }
            }
            .navigationBarHidden(true)
            .onAppear {
                animateCharacter = true
            }
            .sheet(isPresented: $showChatView) {
                NavigationView {
                    ChatView()
                }
            }
            .sheet(isPresented: $showReportView) {
                NavigationView {
                    ReportView()
                }
            }
            .sheet(isPresented: $showCheckupView) {
                NavigationView {
                    CheckupView()
                }
            }
            .overlay(
                // Menu Overlay
                Group {
                    if showMenu {
                        MenuView(
                            isPresented: $showMenu,
                            onChatTapped: {
                                showChatView = true
                            },
                            onReportTapped: {
                                showReportView = true
                            },
                            onCheckupTapped: {
                                showCheckupView = true
                            }
                        )
                        .transition(.asymmetric(
                            insertion: .move(edge: .trailing).combined(with: .opacity),
                            removal: .move(edge: .trailing).combined(with: .opacity)
                        ))
                        .animation(.easeInOut(duration: 0.3), value: showMenu)
                        .zIndex(1)
                        .onTapGesture {
                            // Prevent menu from closing when tapping menu items
                        }
                    }
                }
            )
        }
    }
}

struct PlantMainCharacterView: View {
    @State private var bounce = false
    @State private var leafSway = false
    
    var body: some View {
        ZStack {
            // 화분 (황갈색 사다리꼴)
            Path { path in
                path.move(to: CGPoint(x: 15, y: 0))
                path.addLine(to: CGPoint(x: 55, y: 0))
                path.addLine(to: CGPoint(x: 65, y: 50))
                path.addLine(to: CGPoint(x: 5, y: 50))
                path.closeSubpath()
            }
            .fill(Color(red: 218/255, green: 165/255, blue: 32/255))
            .frame(width: 70, height: 50)
            .offset(y: 25)
            
            // 식물 머리 (베이지색 원)
            Circle()
                .fill(Color(red: 222/255, green: 184/255, blue: 135/255))
                .frame(width: 60, height: 60)
                .overlay(
                    // 눈 두 개
                    HStack(spacing: 12) {
                        Circle()
                            .fill(Color.black)
                            .frame(width: 4, height: 4)
                        Circle()
                            .fill(Color.black)
                            .frame(width: 4, height: 4)
                    }
                    .offset(y: -2)
                )
                .offset(y: bounce ? -2 : 2)
                .animation(.easeInOut(duration: 2.0).repeatForever(autoreverses: true), value: bounce)
            
            // 왼쪽 잎사귀
            Ellipse()
                .fill(Color(red: 34/255, green: 139/255, blue: 34/255))
                .frame(width: 16, height: 24)
                .rotationEffect(.degrees(-30))
                .offset(x: -20, y: -25)
                .rotationEffect(.degrees(leafSway ? -5 : 5))
                .animation(.easeInOut(duration: 1.5).repeatForever(autoreverses: true), value: leafSway)
            
            // 오른쪽 잎사귀
            Ellipse()
                .fill(Color(red: 34/255, green: 139/255, blue: 34/255))
                .frame(width: 16, height: 24)
                .rotationEffect(.degrees(30))
                .offset(x: 20, y: -25)
                .rotationEffect(.degrees(leafSway ? 5 : -5))
                .animation(.easeInOut(duration: 1.8).repeatForever(autoreverses: true), value: leafSway)
        }
        .frame(width: 80, height: 80)
        .onAppear {
            bounce = true
            leafSway = true
        }
    }
}

struct CalendarView: View {
    @Binding var selectedDate: Int
    let dates: [Int]
    
    var body: some View {
        VStack(spacing: 0) {
            // Calendar Header
            HStack {
                Rectangle()
                    .fill(Color(red: 157/255, green: 175/255, blue: 131/255))
                    .frame(height: 16)
                    .cornerRadius(15, corners: [.topLeft, .topRight])
                
                Spacer()
                
                Button(action: {}) {
                    Image(systemName: "chevron.right")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundColor(.black)
                }
                .padding(.trailing, 8)
            }
            .frame(height: 16)
            
            // Calendar Dates
            HStack(spacing: 0) {
                ForEach(dates, id: \.self) { date in
                    VStack(spacing: 8) {
                        Rectangle()
                            .fill(Color.gray.opacity(0.3))
                            .frame(width: 1, height: 27)
                        
                        Text("\(date)")
                            .font(.system(size: 16, weight: .medium))
                            .foregroundColor(
                                date == 21 ? Color.blue :
                                date == 22 ? Color.red :
                                Color.black
                            )
                    }
                    .frame(maxWidth: .infinity)
                    .onTapGesture {
                        selectedDate = date
                    }
                }
            }
            .padding(.horizontal, 8)
            .padding(.vertical, 12)
            .background(Color.white)
            .cornerRadius(15, corners: [.bottomLeft, .bottomRight])
        }
        .cornerRadius(15)
    }
}

extension View {
    func cornerRadius(_ radius: CGFloat, corners: UIRectCorner) -> some View {
        clipShape(RoundedCorner(radius: radius, corners: corners))
    }
}

struct RoundedCorner: Shape {
    var radius: CGFloat = .infinity
    var corners: UIRectCorner = .allCorners

    func path(in rect: CGRect) -> Path {
        let path = UIBezierPath(
            roundedRect: rect,
            byRoundingCorners: corners,
            cornerRadii: CGSize(width: radius, height: radius)
        )
        return Path(path.cgPath)
    }
}

#Preview {
    ContentView()
} 