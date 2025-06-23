import SwiftUI

struct ReportView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var showMenu = false
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Background
                Color(red: 234/255, green: 230/255, blue: 213/255)
                    .ignoresSafeArea()
                
                ScrollView {
                    VStack(spacing: 0) {
                        // Status Bar 영역
                        Rectangle()
                            .fill(Color.clear)
                            .frame(height: 62)
                        
                        // Header
                        HStack {
                            // Back Button
                            Button(action: {
                                dismiss()
                            }) {
                                Image(systemName: "chevron.left")
                                    .font(.system(size: 20, weight: .medium))
                                    .foregroundColor(.black)
                            }
                            
                            Spacer()
                            
                            Text("Report")
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
                        
                        VStack(spacing: 24) {
                            // Date
                            HStack {
                                Text("2025년 6월 21일 (토)")
                                    .font(.system(size: 12))
                                    .foregroundColor(.black)
                                Spacer()
                            }
                            .padding(.horizontal, 32)
                            
                            // Plant Info Section
                            VStack(spacing: 16) {
                                Text("스킨답서스")
                                    .font(.system(size: 10))
                                    .foregroundColor(.black)
                                
                                Text("그루트")
                                    .font(.system(size: 20, weight: .medium))
                                    .foregroundColor(.black)
                                
                                // Plant Character
                                PlantReportCharacterView()
                                    .frame(height: 145)
                                
                                Text("그루트와 친구된 지 00일 째")
                                    .font(.system(size: 12))
                                    .foregroundColor(.black)
                            }
                            .padding(.bottom, 20)
                            
                            // Current Environment Section
                            VStack(alignment: .leading, spacing: 16) {
                                HStack {
                                    Circle()
                                        .fill(Color.black)
                                        .frame(width: 4, height: 4)
                                    Text("현재 환경 지표")
                                        .font(.system(size: 16, weight: .bold))
                                        .foregroundColor(.black)
                                    Spacer()
                                }
                                .padding(.horizontal, 32)
                                
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
                                .cornerRadius(10)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 10)
                                        .stroke(Color(red: 3/255, green: 158/255, blue: 8/255), lineWidth: 2)
                                )
                                .padding(.horizontal, 32)
                            }
                            
                            // Temperature Trend
                            ChartSectionView(title: "7일 간 온도 트렌드")
                            
                            // Humidity Trend
                            ChartSectionView(title: "7일 간 습도 트렌드")
                            
                            // Light Trend
                            ChartSectionView(title: "7일 간 조도 트렌드")
                            
                            // Bottom spacing
                            Rectangle()
                                .fill(Color.clear)
                                .frame(height: 60)
                        }
                    }
                }
            }
        }
        .navigationBarHidden(true)
        .overlay(
            // Menu Overlay
            Group {
                if showMenu {
                    MenuView(
                        isPresented: $showMenu,
                        onChatTapped: {
                            // 채팅 화면으로 이동 (필요시 구현)
                        },
                        onReportTapped: {
                            // 이미 리포트 화면이므로 아무것도 하지 않음
                        },
                        onCheckupTapped: {
                            // 체크업 화면으로 이동 (필요시 구현)
                        }
                    )
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .trailing).combined(with: .opacity)
                    ))
                    .animation(.easeInOut(duration: 0.3), value: showMenu)
                    .zIndex(1)
                }
            }
        )
    }
}

struct PlantReportCharacterView: View {
    @State private var bounce = false
    @State private var leafSway = false
    
    var body: some View {
        ZStack {
            // 화분 (황갈색 사다리꼴)
            Path { path in
                path.move(to: CGPoint(x: 20, y: 0))
                path.addLine(to: CGPoint(x: 80, y: 0))
                path.addLine(to: CGPoint(x: 90, y: 60))
                path.addLine(to: CGPoint(x: 10, y: 60))
                path.closeSubpath()
            }
            .fill(Color(red: 218/255, green: 165/255, blue: 32/255))
            .frame(width: 100, height: 60)
            .offset(y: 30)
            
            // 식물 머리 (베이지색 원)
            Circle()
                .fill(Color(red: 222/255, green: 184/255, blue: 135/255))
                .frame(width: 80, height: 80)
                .overlay(
                    // 눈 두 개
                    HStack(spacing: 16) {
                        Circle()
                            .fill(Color.black)
                            .frame(width: 5, height: 5)
                        Circle()
                            .fill(Color.black)
                            .frame(width: 5, height: 5)
                    }
                    .offset(y: -3)
                )
                .offset(y: bounce ? -3 : 3)
                .animation(.easeInOut(duration: 2.0).repeatForever(autoreverses: true), value: bounce)
            
            // 왼쪽 잎사귀
            Ellipse()
                .fill(Color(red: 34/255, green: 139/255, blue: 34/255))
                .frame(width: 20, height: 30)
                .rotationEffect(.degrees(-30))
                .offset(x: -28, y: -35)
                .rotationEffect(.degrees(leafSway ? -5 : 5))
                .animation(.easeInOut(duration: 1.5).repeatForever(autoreverses: true), value: leafSway)
            
            // 오른쪽 잎사귀
            Ellipse()
                .fill(Color(red: 34/255, green: 139/255, blue: 34/255))
                .frame(width: 20, height: 30)
                .rotationEffect(.degrees(30))
                .offset(x: 28, y: -35)
                .rotationEffect(.degrees(leafSway ? 5 : -5))
                .animation(.easeInOut(duration: 1.8).repeatForever(autoreverses: true), value: leafSway)
        }
        .frame(width: 120, height: 120)
        .onAppear {
            bounce = true
            leafSway = true
        }
    }
}

struct ChartSectionView: View {
    let title: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Circle()
                    .fill(Color.black)
                    .frame(width: 4, height: 4)
                Text(title)
                    .font(.system(size: 16, weight: .bold))
                    .foregroundColor(.black)
                Spacer()
            }
            .padding(.horizontal, 32)
            
            // Chart Container
            VStack(spacing: 0) {
                // Chart Area
                ZStack {
                    // Background
                    Rectangle()
                        .fill(Color.white)
                        .frame(height: 131)
                        .cornerRadius(10)
                    
                    // Grid Lines (simplified)
                    VStack(spacing: 15) {
                        ForEach(0..<6) { _ in
                            Rectangle()
                                .fill(Color.gray.opacity(0.2))
                                .frame(height: 0.5)
                        }
                    }
                    .padding(.horizontal, 20)
                    
                    // Chart Line (simplified green area)
                    Rectangle()
                        .fill(Color(red: 3/255, green: 158/255, blue: 8/255).opacity(0.28))
                        .frame(height: 28)
                        .cornerRadius(4)
                        .padding(.horizontal, 20)
                        .offset(y: 10)
                    
                    // Data Points
                    HStack(spacing: 35) {
                        ForEach(0..<7) { index in
                            Circle()
                                .fill(Color(red: 3/255, green: 158/255, blue: 8/255))
                                .frame(width: 5, height: 5)
                                .offset(y: CGFloat.random(in: -15...15))
                        }
                    }
                    .padding(.horizontal, 20)
                    
                    // Y-axis labels
                    HStack {
                        VStack(spacing: 12) {
                            ForEach(["40", "30", "20", "10", "0"], id: \.self) { value in
                                Text(value)
                                    .font(.system(size: 5))
                                    .foregroundColor(.black)
                            }
                        }
                        .padding(.leading, 10)
                        
                        Spacer()
                    }
                    
                    // X-axis labels
                    VStack {
                        Spacer()
                        
                        HStack(spacing: 25) {
                            ForEach(["06.15", "06.16", "06.17", "06.18", "06.19", "06.20", "06.21"], id: \.self) { date in
                                Text(date)
                                    .font(.system(size: 5))
                                    .foregroundColor(.black)
                                    .frame(maxWidth: .infinity)
                            }
                        }
                        .padding(.horizontal, 20)
                        .padding(.bottom, 8)
                    }
                }
            }
            .padding(.horizontal, 32)
        }
    }
}

#Preview {
    ReportView()
} 