import SwiftUI

struct MenuView: View {
    @Binding var isPresented: Bool
    let onChatTapped: () -> Void
    let onReportTapped: () -> Void
    let onCheckupTapped: () -> Void
    
    var body: some View {
        ZStack {
            // Background overlay
            Color.black.opacity(0.72)
                .ignoresSafeArea()
                .onTapGesture {
                    isPresented = false
                }
            
            HStack(spacing: 0) {
                // Left side (dimmed area)
                Rectangle()
                    .fill(Color.clear)
                    .frame(width: 118)
                    .onTapGesture {
                        isPresented = false
                    }
                
                // Menu Panel
                VStack(spacing: 0) {
                    // Status Bar 영역
                    Rectangle()
                        .fill(Color.clear)
                        .frame(height: 62)
                    
                    // Menu Header
                    HStack {
                        Button(action: {}) {
                            Image(systemName: "line.3.horizontal")
                                .font(.system(size: 30))
                                .foregroundColor(.black)
                        }
                        
                        Spacer()
                        
                        Text("MENU")
                            .font(.system(size: 24, weight: .bold))
                            .foregroundColor(.black)
                        
                        Spacer()
                        
                        Button(action: {
                            isPresented = false
                        }) {
                            Image(systemName: "house.fill")
                                .font(.system(size: 28))
                                .foregroundColor(.black)
                        }
                    }
                    .padding(.horizontal, 20)
                    .padding(.bottom, 30)
                    
                    // Menu Items
                    VStack(spacing: 0) {
                        // PLANTCHAT Section
                        VStack(alignment: .leading, spacing: 12) {
                            Text("PLANTCHAT")
                                .font(.system(size: 20, weight: .bold))
                                .foregroundColor(.black)
                            
                            Button(action: {
                                isPresented = false
                                onChatTapped()
                            }) {
                                HStack(spacing: 12) {
                                    // Plant Character (Small)
                                    ZStack {
                                        // 화분 (황갈색 사다리꼴)
                                        Path { path in
                                            path.move(to: CGPoint(x: 8, y: 22))
                                            path.addLine(to: CGPoint(x: 36, y: 22))
                                            path.addLine(to: CGPoint(x: 40, y: 44))
                                            path.addLine(to: CGPoint(x: 4, y: 44))
                                            path.closeSubpath()
                                        }
                                        .fill(Color(red: 218/255, green: 165/255, blue: 32/255))
                                        .frame(width: 44, height: 44)
                                        
                                        // 식물 머리 (베이지색 원)
                                        Circle()
                                            .fill(Color(red: 222/255, green: 184/255, blue: 135/255))
                                            .frame(width: 30, height: 30)
                                            .overlay(
                                                HStack(spacing: 6) {
                                                    Circle()
                                                        .fill(Color.black)
                                                        .frame(width: 2, height: 2)
                                                    Circle()
                                                        .fill(Color.black)
                                                        .frame(width: 2, height: 2)
                                                }
                                                .offset(y: -1)
                                            )
                                            .offset(y: -7)
                                        
                                        // 왼쪽 잎사귀
                                        Ellipse()
                                            .fill(Color(red: 34/255, green: 139/255, blue: 34/255))
                                            .frame(width: 8, height: 12)
                                            .rotationEffect(.degrees(-30))
                                            .offset(x: -10, y: -18)
                                        
                                        // 오른쪽 잎사귀
                                        Ellipse()
                                            .fill(Color(red: 34/255, green: 139/255, blue: 34/255))
                                            .frame(width: 8, height: 12)
                                            .rotationEffect(.degrees(30))
                                            .offset(x: 10, y: -18)
                                    }
                                    
                                    VStack(alignment: .leading, spacing: 4) {
                                        Text("그루트")
                                            .font(.system(size: 15, weight: .bold))
                                            .foregroundColor(.black)
                                        
                                        Text("스킨답서스")
                                            .font(.system(size: 10))
                                            .foregroundColor(.black)
                                    }
                                    
                                    Spacer()
                                    
                                    Text("Mate Date : 2025.06.21")
                                        .font(.system(size: 10))
                                        .foregroundColor(.black)
                                }
                            }
                        }
                        .padding(.horizontal, 20)
                        .padding(.bottom, 30)
                        
                        // Menu Options
                        VStack(spacing: 24) {
                            // REPORT
                            Button(action: {
                                isPresented = false
                                onReportTapped()
                            }) {
                                MenuItemContentView(title: "REPORT")
                            }
                            
                            // CHECKUP
                            Button(action: {
                                isPresented = false
                                onCheckupTapped()
                            }) {
                                MenuItemContentView(title: "CHECKUP")
                            }
                        }
                        .padding(.horizontal, 20)
                        
                        Spacer()
                    }
                    
                    // Home Indicator 영역
                    Rectangle()
                        .fill(Color.clear)
                        .frame(height: 34)
                }
                .frame(width: 282)
                .background(Color(red: 234/255, green: 230/255, blue: 213/255))
            }
        }
        .navigationBarHidden(true)
    }
}

struct MenuItemView: View {
    let title: String
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            HStack {
                Text(title)
                    .font(.system(size: 20, weight: .bold))
                    .foregroundColor(.black)
                
                Spacer()
                
                Image(systemName: "chevron.right")
                    .font(.system(size: 19))
                    .foregroundColor(.black)
            }
        }
    }
}

struct MenuItemContentView: View {
    let title: String
    
    var body: some View {
        HStack {
            Text(title)
                .font(.system(size: 20, weight: .bold))
                .foregroundColor(.black)
            
            Spacer()
            
            Image(systemName: "chevron.right")
                .font(.system(size: 19))
                .foregroundColor(.black)
        }
    }
}

#Preview {
    MenuView(
        isPresented: .constant(true),
        onChatTapped: {},
        onReportTapped: {},
        onCheckupTapped: {}
    )
} 