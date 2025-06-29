import styles from "./header.module.css";

function ChatHeader() {
  return (
    <div className={styles.chatheader}>
      <div className={styles.imgBackground}>
        <img
          className={styles.headerImg}
          src="https://cdn-icons-png.flaticon.com/512/8554/8554115.png"
        />
      </div>
      <div className={styles.headerText}>
        <h2>AI Philosopher</h2>
        <div>Exploring the depths of consciousness</div>
      </div>
    </div>
  );
}

export default ChatHeader;
