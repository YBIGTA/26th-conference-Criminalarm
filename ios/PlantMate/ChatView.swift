import SwiftUI

struct ChatView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var messageText = ""
    @State private var showTypingIndicator = true
    @State private var animateDots = false
    @State private var showMenu = false
    
    let messages = [
        ChatMessage(id: 1, text: "여~ 히사시부리다네~", isFromUser: false, timestamp: Date()),
        ChatMessage(id: 2, text: "그루트야 컨디션은 좀 어때", isFromUser: true, timestamp: Date())
    ]
    
    var body: some View {
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
                        // Back Button - 메인 화면으로 돌아가기
                        Button(action: {
                            dismiss()
                        }) {
                            Image(systemName: "chevron.left")
                                .font(.system(size: 20, weight: .medium))
                                .foregroundColor(.black)
                        }
                        
                        VStack(alignment: .leading, spacing: 4) {
                            Text("PlantChat")
                                .font(.system(size: 32, weight: .regular, design: .rounded))
                                .foregroundColor(Color(red: 3/255, green: 158/255, blue: 8/255))
                            
                            Text("with 그루트")
                                .font(.system(size: 12, weight: .regular))
                                .foregroundColor(.black)
                        }
                        
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
                    
                    // Chat Content
                    ScrollView {
                        VStack(spacing: 16) {
                            // Date Header
                            HStack {
                                Spacer()
                                Text("2025년 6월 21일 (토)")
                                    .font(.system(size: 10, weight: .regular))
                                    .foregroundColor(.black)
                                    .padding(.horizontal, 16)
                                    .padding(.vertical, 4)
                                    .background(Color.black.opacity(0.18))
                                    .cornerRadius(15)
                                Spacer()
                            }
                            .padding(.top, 16)
                            
                            // Messages
                            VStack(spacing: 16) {
                                ForEach(messages) { message in
                                    ChatMessageView(message: message)
                                }
                                
                                // Typing Indicator
                                if showTypingIndicator {
                                    TypingIndicatorView(animateDots: $animateDots)
                                }
                            }
                            .padding(.horizontal, 20)
                        }
                    }
                    
                    Spacer()
                    
                    // Message Input
                    ChatInputView(messageText: $messageText) {
                        // Send message action
                        sendMessage()
                    }
                    .padding(.horizontal, 20)
                    .padding(.bottom, 20)
                    
                    // Home Indicator 영역
                    Rectangle()
                        .fill(Color.clear)
                        .frame(height: 34)
                }
            }
        }
        .navigationBarHidden(true)
        .onAppear {
            animateDots = true
        }
        .overlay(
            // Menu Overlay
            Group {
                if showMenu {
                    MenuView(
                        isPresented: $showMenu,
                        onChatTapped: {
                            // 이미 채팅 화면이므로 아무것도 하지 않음
                        },
                        onReportTapped: {
                            // 리포트 화면으로 이동 (필요시 구현)
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
    
    private func sendMessage() {
        // 메시지 전송 로직
        messageText = ""
    }
}

struct ChatMessage: Identifiable {
    let id: Int
    let text: String
    let isFromUser: Bool
    let timestamp: Date
}

struct ChatMessageView: View {
    let message: ChatMessage
    
    var body: some View {
                    if message.isFromUser {
                HStack(alignment: .top, spacing: 8) {
                    Spacer()
                    
                    // User message bubble
                    Text(message.text)
                        .font(.system(size: 16))
                        .foregroundColor(.white)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 12)
                        .background(Color(red: 3/255, green: 158/255, blue: 8/255))
                        .cornerRadius(20, corners: [.topLeft, .bottomLeft, .bottomRight])
                }
            } else {
                HStack(alignment: .top, spacing: 8) {
                    // Plant character avatar
                    PlantChatCharacterView()
                        .frame(width: 44, height: 44)
                    
                    // Plant message bubble
                    Text(message.text)
                        .font(.system(size: 16))
                        .foregroundColor(.black)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 12)
                        .background(Color.white)
                        .cornerRadius(20, corners: [.topRight, .bottomLeft, .bottomRight])
                        .overlay(
                            RoundedRectangle(cornerRadius: 20)
                                .stroke(Color.gray.opacity(0.2), lineWidth: 1)
                        )
                    
                    Spacer()
                }
            }
    }
}

struct TypingIndicatorView: View {
    @Binding var animateDots: Bool
    
    var body: some View {
        HStack {
            // Plant character
            PlantChatCharacterView()
                .frame(width: 44, height: 44)
            
            // Typing dots
            HStack(spacing: 4) {
                ForEach(0..<3) { index in
                    Circle()
                        .fill(Color.gray)
                        .frame(width: 6, height: 6)
                        .scaleEffect(animateDots ? 1.2 : 0.8)
                        .animation(
                            .easeInOut(duration: 0.6)
                            .repeatForever(autoreverses: true)
                            .delay(Double(index) * 0.2),
                            value: animateDots
                        )
                }
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(Color.white)
            .cornerRadius(10)
            
            Spacer()
        }
    }
}

struct PlantChatCharacterView: View {
    @State private var bounce = false
    @State private var leafSway = false
    
    var body: some View {
        ZStack {
            // 화분 (황갈색 사다리꼴)
            Path { path in
                path.move(to: CGPoint(x: 6, y: 0))
                path.addLine(to: CGPoint(x: 24, y: 0))
                path.addLine(to: CGPoint(x: 28, y: 22))
                path.addLine(to: CGPoint(x: 2, y: 22))
                path.closeSubpath()
            }
            .fill(Color(red: 218/255, green: 165/255, blue: 32/255))
            .frame(width: 30, height: 22)
            .offset(y: 11)
            
            // 식물 머리 (베이지색 원)
            Circle()
                .fill(Color(red: 222/255, green: 184/255, blue: 135/255))
                .frame(width: 26, height: 26)
                .overlay(
                    // 눈 두 개
                    HStack(spacing: 5) {
                        Circle()
                            .fill(Color.black)
                            .frame(width: 2, height: 2)
                        Circle()
                            .fill(Color.black)
                            .frame(width: 2, height: 2)
                    }
                    .offset(y: -1)
                )
                .offset(y: bounce ? -1 : 1)
                .animation(.easeInOut(duration: 2.0).repeatForever(autoreverses: true), value: bounce)
            
            // 왼쪽 잎사귀
            Ellipse()
                .fill(Color(red: 34/255, green: 139/255, blue: 34/255))
                .frame(width: 7, height: 10)
                .rotationEffect(.degrees(-30))
                .offset(x: -8, y: -11)
                .rotationEffect(.degrees(leafSway ? -3 : 3))
                .animation(.easeInOut(duration: 1.5).repeatForever(autoreverses: true), value: leafSway)
            
            // 오른쪽 잎사귀
            Ellipse()
                .fill(Color(red: 34/255, green: 139/255, blue: 34/255))
                .frame(width: 7, height: 10)
                .rotationEffect(.degrees(30))
                .offset(x: 8, y: -11)
                .rotationEffect(.degrees(leafSway ? 3 : -3))
                .animation(.easeInOut(duration: 1.8).repeatForever(autoreverses: true), value: leafSway)
        }
        .frame(width: 35, height: 35)
        .onAppear {
            bounce = true
            leafSway = true
        }
    }
}

struct ChatInputView: View {
    @Binding var messageText: String
    let onSend: () -> Void
    
    var body: some View {
        HStack(spacing: 8) {
            // Text input
            TextField("메시지를 입력하세요...", text: $messageText)
                .font(.system(size: 14))
                .padding(.horizontal, 16)
                .padding(.vertical, 12)
                .background(Color.white)
                .cornerRadius(26)
            
            // Send button
            Button(action: onSend) {
                Image(systemName: "paperplane.fill")
                    .font(.system(size: 20))
                    .foregroundColor(Color(red: 3/255, green: 158/255, blue: 8/255))
                    .frame(width: 31, height: 31)
            }
            .disabled(messageText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
        }
    }
}

#Preview {
    ChatView()
} 