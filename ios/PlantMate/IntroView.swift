import SwiftUI

struct IntroView: View {
    @Binding var showIntro: Bool
    @State private var animateCharacter = false
    @State private var animateText = false
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Background - Figma의 베이지 색상
                Color(red: 234/255, green: 230/255, blue: 213/255)
                    .ignoresSafeArea()
                
                VStack(spacing: 0) {
                    // Status Bar 영역
                    Rectangle()
                        .fill(Color.clear)
                        .frame(height: 62)
                    
                    Spacer()
                    
                    // 메인 콘텐츠
                    VStack(spacing: 20) {
                        // 부제목
                        Text("반려식물을 위한 AI 가드너")
                            .font(.system(size: 15, weight: .regular))
                            .foregroundColor(.black)
                            .opacity(animateText ? 1.0 : 0.0)
                            .offset(y: animateText ? 0 : 20)
                            .animation(.easeOut(duration: 0.8).delay(0.3), value: animateText)
                        
                        // 메인 타이틀
                        Text("PlantMate")
                            .font(.system(size: 40, weight: .regular, design: .rounded))
                            .foregroundColor(Color(red: 3/255, green: 158/255, blue: 8/255))
                            .opacity(animateText ? 1.0 : 0.0)
                            .offset(y: animateText ? 0 : 30)
                            .animation(.easeOut(duration: 0.8).delay(0.5), value: animateText)
                        
                        // 식물 캐릭터
                        PlantCharacterView()
                            .scaleEffect(animateCharacter ? 1.0 : 0.3)
                            .opacity(animateCharacter ? 1.0 : 0.0)
                            .animation(.spring(response: 0.8, dampingFraction: 0.6).delay(0.8), value: animateCharacter)
                    }
                    
                    Spacer()
                    
                    // 탭하여 시작하기 (선택사항)
                    Button(action: {
                        withAnimation(.spring(response: 0.6, dampingFraction: 0.8)) {
                            showIntro = false
                        }
                    }) {
                        Text("화면을 탭하여 시작하기")
                            .font(.system(size: 16, weight: .medium))
                            .foregroundColor(.black.opacity(0.6))
                            .padding(.bottom, 60)
                    }
                    .opacity(animateText ? 0.8 : 0.0)
                    .animation(.easeOut(duration: 0.8).delay(1.2), value: animateText)
                    
                    // Home Indicator 영역
                    Rectangle()
                        .fill(Color.clear)
                        .frame(height: 34)
                }
            }
        }
        .onAppear {
            animateText = true
            animateCharacter = true
        }
        .onTapGesture {
            withAnimation(.spring(response: 0.6, dampingFraction: 0.8)) {
                showIntro = false
            }
        }
    }
}

struct PlantCharacterView: View {
    @State private var bounce = false
    @State private var leafSway = false
    
    var body: some View {
        ZStack {
            // 화분 (베이지색 원형)
            Circle()
                .fill(Color(red: 220/255, green: 196/255, blue: 176/255))
                .frame(width: 80, height: 80)
                .offset(y: bounce ? -2 : 2)
                .animation(.easeInOut(duration: 2.0).repeatForever(autoreverses: true), value: bounce)
            
            // 눈 (왼쪽)
            Circle()
                .fill(Color.black)
                .frame(width: 6, height: 6)
                .offset(x: -12, y: -5)
            
            // 눈 (오른쪽)
            Circle()
                .fill(Color.black)
                .frame(width: 6, height: 6)
                .offset(x: 12, y: -5)
            
            // 잎사귀들
            VStack(spacing: -5) {
                // 위쪽 잎사귀
                Image(systemName: "leaf.fill")
                    .font(.system(size: 20))
                    .foregroundColor(Color(red: 3/255, green: 158/255, blue: 8/255))
                    .rotationEffect(.degrees(leafSway ? -5 : 5))
                    .animation(.easeInOut(duration: 1.5).repeatForever(autoreverses: true), value: leafSway)
                
                // 아래쪽 잎사귀
                Image(systemName: "leaf.fill")
                    .font(.system(size: 16))
                    .foregroundColor(Color(red: 34/255, green: 139/255, blue: 34/255))
                    .rotationEffect(.degrees(leafSway ? 3 : -3))
                    .animation(.easeInOut(duration: 1.8).repeatForever(autoreverses: true), value: leafSway)
            }
            .offset(x: 25, y: -30)
        }
        .onAppear {
            bounce = true
            leafSway = true
        }
    }
}

#Preview {
    IntroView(showIntro: .constant(true))
} 